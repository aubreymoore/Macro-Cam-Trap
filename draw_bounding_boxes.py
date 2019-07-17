#!/usr/bin/env python
# coding: utf-8

# In[60]:


import pandas as pd
import cv2
import argparse
import sys


# In[61]:


# The following line allows testing argparse within a Jupyter notebook
# Comment it out when using code in a script
#sys.argv = ['draw_bounding_boxes', '/media/aubrey/70D7-5135/videos', '1563341307489']

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


# In[62]:


# Load bounding_boxes.csv into a data frame.
fn = '{}/{}/bounding_boxes.csv'.format(args.data_dir, args.video_timestamp)
df = pd.read_csv(fn)
#df


# In[63]:


# Get dimensions of first frame, we assume that all frames have the same size.
path = '{}/{}'.format(mydir, df['filename'][0])
#print(path)
img = cv2.imread(path)
frame_height, frame_width, _ = img.shape
#print('frame_height: {}, frame_width: {}'.format(frame_height, frame_width))


# In[64]:


# Convert coordinates from proportions to pixels
df['xtl'] = df['xtl'].apply(lambda x: int(x * frame_width))
df['ytl'] = df['ytl'].apply(lambda x: int(x * frame_height))
df['xbr'] = df['xbr'].apply(lambda x: int(x * frame_width))
df['ybr'] = df['ybr'].apply(lambda x: int(x * frame_height))


# In[65]:


# Group by frame
grouped = df.groupby('filename')


# In[66]:


# Iterate over frames
for name, df_group in grouped:
    img = cv2.imread(name, cv2.IMREAD_UNCHANGED)
    
    # Draw bounding boxes on each frame
    for index, row in df_group.iterrows():
        filename, xtl, ytl, xbr, ybr = row
        cv2.rectangle(img, (xtl, ytl), (xbr, ybr), (0, 255, 0), 3)

    # Show image with bounding boxes
    cv2.imshow(mydir, img)
    cv2.waitKey(args.delay_ms)

cv2.destroyAllWindows()


# In[52]:


#get_ipython().system("jupyter nbconvert --to=script 'draw_bounding_boxes.ipynb'")


# In[ ]:




