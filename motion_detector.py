#!/usr/bin/env python
# coding: utf-8

# In[10]:


import imutils
import time
import cv2
import argparse
import os
import shutil
import pandas as pd
import sys


# In[11]:


start = time.time()


# In[12]:


# The following line allows testing argparse within a Jupyter notebook
# Comment it out when using code in a script
sys.argv = ['motion_detector.py', '/media/aubrey/70D7-5135/videos', '1563341307489']

parser = argparse.ArgumentParser(description='Motion detector.    When one or more objects in motion are detected in a video frame,    the frame is saved and bounding box coordinates are added to a dataframe.    When the video has been processed, the dataframe is saved as a CSV file    and the original video is optionally deleted to save storage space.    This script should be run in the same directory as the video file.')

parser.add_argument('data_dir',
                    type=str,
                    help='data directory (without trailing /) \
                    Example: /media/pi/9016-4EF8/videos')
  
parser.add_argument('video_timestamp',
                    type=str,
                    help='video timestamp \
                    Example: 1562836438727')

parser.add_argument('--frame_size_factor',
                    default=4,
                    help='the frame size is shrunken by this factor before \
                    motion detection is performed to speed up processing \
                    (default=4).')

parser.add_argument('--min_area',
                    default=0.001,
                    help='minimum size of moving object in relation to area of full frame \
                    frame (default=0.001)')

parser.add_argument('--keep_video',
                    default='true',
                    help='keep the original video after processing?')
                    
args = parser.parse_args()


# In[14]:


video_file_path = '{}/{}/{}.h264'.format(args.data_dir, args.video_timestamp, args.video_timestamp)
vs = cv2.VideoCapture(video_file_path)
original_frame_width = vs.get(3)
original_frame_height = vs.get(4)
detection_frame_width = int(original_frame_width / args.frame_size_factor)
detection_frame_height = int(original_frame_height / args.frame_size_factor)
detection_minimum_area = int(args.min_area * detection_frame_width * detection_frame_height)

# initialize the first frame in the video stream
firstFrame = None

# Create an empty dataframe to store bounding boxes for objects in motion
df = pd.DataFrame(columns=['filename', 'xtl', 'ytl', 'xbr', 'ybr'])

# loop over the frames of the video
framenum = 0
avg = None
while True:
    # grab the current frame
    frame = vs.read()
    frame = frame[1]
    
    # If we are at the end of the file, the frame will be empty, so break out of the loop.
    if frame is None:
        break
    
    # Increment the frame count and print every 100 frames to indicate progress.
    framenum += 1
    if (framenum % 100) == 0:
        print('{} frames processed'.format((framenum)))

    # resize the frame, convert it to grayscale, and blur it
    # a copy of the original frame is saved temporarily
    original_frame = frame
    frame = imutils.resize(frame, width=detection_frame_width)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    # if the average frame is None, initialize
    if avg is None:
        # print("[INFO] starting background model...")
        avg = gray.copy().astype("float")
        #rawCapture.truncate(0)
        continue    
    
    # accumulate the weighted average between the current frame and previous frames, 
    # then compute the difference between the current frame and running average
    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))    
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    bbfound = False
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) > detection_minimum_area:
            bbfound = True

            # compute the bounding box for the contour with coordinates
            # expressed as proportion of width and height of frame
            (x, y, w, h) = cv2.boundingRect(c)
            xtl = x / detection_frame_width
            ytl = y / detection_frame_height
            xbr = (x+w) / detection_frame_width
            ybr = (y+h) / detection_frame_height
            filename = '{}f{:0>6}.jpg'.format(args.video_timestamp, framenum)
            print('mob {} {:f} {:f} {:f} {:f}'.format(filename, xtl, ytl, xbr, ybr))
            df = df.append({'filename': filename,
                            'xtl': xtl,
                            'ytl': ytl,
                            'xbr': xbr,
                            'ybr': ybr},
                            ignore_index=True)
    # if one ot more moving objects were detected, save the original frame
    if bbfound:
        cv2.imwrite(filename, original_frame)

# Save the dataframe as a CSV        
filename ='{}/{}/bounding_boxes.csv'.format(args.data_dir, args.video_timestamp)
print('Saving bounding box data to ' + filename)
df.to_csv(filename, index=False)

vs.release()

if args.keep_video=='false':
    os.remove(video_file_path)
    print('{} deleted'.format(video_file_path))

# Display run time
print('Processing time: {} seconds'.format(int(time.time()-start)))


# In[ ]:


get_ipython().system("jupyter nbconvert --to=script 'motion_detector'")

