#!/bin/bash




import pandas as pd
import cv2
import myfunctions
import argeparse

# Load bounding_boxes.csv into a data frame.
fn = 'bees.h264_frames/bounding_boxes.csv'
df = pd.read_csv(fn)
print(df)
quit()

# Get dimensions of first frame, we assume that all frames have the same size.
fn = df['filename'][0]
img = cv2.imread(fn)
frame_width, frame_height, _ = img.shape
#print('{},{}'.format(frame_width, frame_height))

# Convert coordinates from proportions to pixels
df['xtl'] = df['xtl'].apply(lambda x: int(x * frame_width))
df['ytl'] = df['ytl'].apply(lambda x: int(x * frame_height))
df['xbr'] = df['xbr'].apply(lambda x: int(x * frame_width))
df['ybr'] = df['ybr'].apply(lambda x: int(x * frame_height))
#print(df)

# Group by frame
grouped = df.groupby('filename')

# Iterate over frames
for name, df_group in grouped:
    print()
    print(name)
    img = cv2.imread(name, cv2.IMREAD_UNCHANGED)
    #print(img.shape)
    #cv2.imshow('a', img)
    #cv2.waitKey(100)
    
    # Draw bounding boxes on each frame
    for index, row in df_group.iterrows():
        img = cv2.imread(name, cv2.IMREAD_UNCHANGED)
        print(row)
        _, xtl, ytl, xbr, ybr = row
        cv2.rectangle(img, (xtl, ytl), (xbr, ybr), (0, 255, 0), 3)

# Show image with bounding boxes
    cv2.imshow('a', img)
    cv2.waitKey(100)

#cv2.imshow(fn, img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()



 
