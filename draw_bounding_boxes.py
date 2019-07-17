#!/usr/bin/env python
# coding: utf-8

# In[46]:


import pandas as pd
import cv2


# In[47]:


mydir = '1563149100286'


# In[48]:


# Load bounding_boxes.csv into a data frame.
fn = '{}/bounding_boxes.csv'.format(dir)
df = pd.read_csv(fn)
#df


# In[49]:


# Get dimensions of first frame, we assume that all frames have the same size.
path = '{}/{}'.format(mydir, df['filename'][0])
print(path)
img = cv2.imread(path)
frame_height, frame_width, _ = img.shape
#print('frame_height: {}, frame_width: {}'.format(frame_height, frame_width))


# In[50]:


# Convert coordinates from proportions to pixels
df['xtl'] = df['xtl'].apply(lambda x: int(x * frame_width))
df['ytl'] = df['ytl'].apply(lambda x: int(x * frame_height))
df['xbr'] = df['xbr'].apply(lambda x: int(x * frame_width))
df['ybr'] = df['ybr'].apply(lambda x: int(x * frame_height))


# In[51]:


# Group by frame
grouped = df.groupby('filename')


# In[52]:


# Iterate over frames
for name, df_group in grouped:
    img = cv2.imread(name, cv2.IMREAD_UNCHANGED)
    
    # Draw bounding boxes on each frame
    for index, row in df_group.iterrows():
        filename, xtl, ytl, xbr, ybr = row
        path = '{}/{}'.format(mydir, filename)
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        cv2.rectangle(img, (xtl, ytl), (xbr, ybr), (0, 255, 0), 3)

# Show image with bounding boxes
    cv2.imshow(mydir, img)
    cv2.waitKey(1000)

cv2.destroyAllWindows()

jupyter nbconvert --to script draw_bounding_boxes.ipynb
# In[2]:


get_ipython().run_cell_magic('bash', '', "jupyter nbconvert --to=script 'draw_bounding_boxes.ipynb'")


# In[ ]:




