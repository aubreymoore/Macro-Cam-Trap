#!/usr/bin/env python
# coding: utf-8

# # Motion Detector
# 
# This Jupyter notebook should be opened using the following commands:
# ~~~bash
#     workon jupyter
#     jupyter notebook
# ~~~

# In[1]:


import imutils
import time
import cv2
import argparse
import os
import shutil
import pandas as pd
import sys
import glob
import logging


# In[2]:


def initiate_logger():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    #formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


# In[3]:


def motion_detector():

    parser = argparse.ArgumentParser(description='Motion detector.        When one or more objects in motion are detected in a video frame,        the frame is saved as a jpg and bounding box coordinates are added to a dataframe.        When the video has been processed, the dataframe is saved as a CSV file        and the original video is optionally deleted to save storage space.')

    parser.add_argument('data_dir',
                        type=str,
                        help='data directory (without trailing /) \
                        Example: /media/aubrey/9016-4EF8/ants')

    parser.add_argument('video_file',
                        type=str,
                        help='video_file name \
                        Example: VID_20190810_120737.mp4')

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

    parser.add_argument('--skip_frames',
                        default=10,
                        help='number of frames to skip at start of recording')

    args = parser.parse_args()

    video_file_path = '{}/{}'.format(args.data_dir, args.video_file)
    vs = cv2.VideoCapture(video_file_path)
    original_frame_width = vs.get(3)
    original_frame_height = vs.get(4)
    detection_frame_width = int(original_frame_width / args.frame_size_factor)
    detection_frame_height = int(original_frame_height / args.frame_size_factor)
    detection_minimum_area = int(args.min_area * detection_frame_width * detection_frame_height)
    skip_frames = args.skip_frames

    # Create a directory for frames in which motion is detected
    frames_dir = '{}/frames'.format(args.data_dir)
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)

    # Create an empty dataframe to store bounding boxes for objects in motion
    df = pd.DataFrame(columns=['filename', 'xtl', 'ytl', 'xbr', 'ybr'])

    fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=50, detectShadows=True)

    # loop over the frames of the video
    logger.debug('Starting motion detector on {}'.format(args.video_file))
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
        if (framenum % 1000) == 0:
            logger.debug('{} frames processed'.format((framenum)))

        # Make a copy of the original frame and resize it
        original_frame = frame
        frame = imutils.resize(frame, width=detection_frame_width)

        # Perform background subtraction
        thresh = fgbg.apply(frame)
        #thresh[thresh==127]=0 # Set shadows (127) to black (0)

        # Find contours on thresholded image
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        if framenum > skip_frames: 
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
                    filename = '{}/frames/{}f{:0>6}.jpg'.format(args.data_dir, args.video_file.split('.')[0], framenum)
                    #print('mob {} {:f} {:f} {:f} {:f}'.format(filename, xtl, ytl, xbr, ybr))
                    df = df.append({'filename': filename,
                                    'xtl': xtl,
                                    'ytl': ytl,
                                    'xbr': xbr,
                                    'ybr': ybr},
                                    ignore_index=True)
            # if one or more moving objects were detected, save the original frame
            if bbfound:
                cv2.imwrite(filename, original_frame)

    # Save the dataframe as a CSV        
    filename ='{}/{}_bounding_boxes.csv'.format(args.data_dir, args.video_file.split('.')[0])
    logger.debug('Saving ' + filename)
    df.to_csv(filename, index=False)

    vs.release()

    if args.keep_video=='false':
        os.remove(video_file)
        logger.debug('{} deleted'.format(video_file))


# In[ ]:


# MAIN

logger = initiate_logger()

# Uncomment the following line to test code within a Jupyter notebook
sys.argv = ['motion_detector.py', 'data/ants/VID_20190810_120737', 'VID_20190810_120737.mp4']

motion_detector()

logger.debug('Finished')


# In[ ]:


# Uncomment the following line to create a pure python script called motion_detector.py
get_ipython().system("jupyter nbconvert --to=script 'motion_detector'")

