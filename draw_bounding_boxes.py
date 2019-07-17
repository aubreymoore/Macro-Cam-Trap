#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import cv2
import argparse
import sys


# In[2]:


# The following line allows testing argparse within a Jupyter notebook
# Comment it out when using code in a script
#sys.argv = ['draw_bounding_boxes', '/media/pi/70D7-5135/videos', '1563341307489']

parser = argparse.ArgumentParser(description='Description goes here.')

parser.add_argument('data_dir',
                    type=str,
                    help='data directory (without trailing /) \
                    Example: /media/pi/9016-4EF8/videos')
  
parser.add_argument('video_timestamp',
                    type=str,
                    help='video timestamp \
                    Example: 1562836438727')

parser.add_argument('--delay_ms',
                    default=100,
                    help='delay between frames in milliseconds (default=100)')
                    
args = parser.parse_args()


# In[3]:


# Load bounding_boxes.csv into a data frame.
fn = '{}/{}/bounding_boxes.csv'.format(args.data_dir, args.video_timestamp)
#print(fn)
df = pd.read_csv(fn)
#df


# In[4]:


# Get dimensions of first frame, we assume that all frames have the same size.
path = '{}/{}/{}'.format(args.data_dir, args.video_timestamp, df['filename'][0])
#print(path)
img = cv2.imread(path)
frame_height, frame_width, _ = img.shape
#print('frame_height: {}, frame_width: {}'.format(frame_height, frame_width))


# In[5]:


# Convert coordinates from proportions to pixels
df['xtl'] = df['xtl'].apply(lambda x: int(x * frame_width))
df['ytl'] = df['ytl'].apply(lambda x: int(x * frame_height))
df['xbr'] = df['xbr'].apply(lambda x: int(x * frame_width))
df['ybr'] = df['ybr'].apply(lambda x: int(x * frame_height))
df


# In[6]:


# Group by frame
grouped = df.groupby('filename')


# In[11]:


# Iterate over frames
for name, df_group in grouped:
    path = '{}/{}/{}'.format(args.data_dir, args.video_timestamp, name)
    #print(path)
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    
    # Draw bounding boxes on each frame
    for index, row in df_group.iterrows():
        filename, xtl, ytl, xbr, ybr = row
        cv2.rectangle(img, (xtl, ytl), (xbr, ybr), (0, 255, 0), 3)

    # Show image with bounding boxes
    cv2.imshow(args.video_timestamp, img)
    cv2.waitKey(args.delay_ms)

cv2.destroyAllWindows()


# In[ ]:


#get_ipython().system("jupyter nbconvert --to=script 'draw_bounding_boxes.ipynb'")


# In[ ]:




