import cv2
import time
import pandas as pd
import os
import shutil

def extract_bb(row, bbnum, mobs_dir):
    img = cv2.imread(row.filename)
    cropped = img[row.ytl:row.ybr, row.xtl:row.xbr]
    fn = row.filename
    fn = fn.replace('_frames', '_mobs')
    fn = fn.replace('.jpg', 'b{:0>6}.jpg'.format(bbnum))
    print(fn)
    cv2.imwrite(fn, cropped)
    return
    
video = 'bees.h264'
frames_dir = video + '_frames'
mobs_dir = video + '_mobs'

if os.path.exists(mobs_dir):
    shutil.rmtree(mobs_dir)
os.makedirs(mobs_dir)

df = pd.read_csv(frames_dir + '/bounding_boxes.csv')

# Convert coordinates from proportions to pixels
img = cv2.imread(df['filename'][0])
img_height, img_width, _ = img.shape
print('width: {} height: {}'.format(img_width, img_height))
df['xtl'] = df['xtl'].apply(lambda x: int(x * img_width))
df['ytl'] = df['ytl'].apply(lambda x: int(x * img_height))
df['xbr'] = df['xbr'].apply(lambda x: int(x * img_width))
df['ybr'] = df['ybr'].apply(lambda x: int(x * img_height))

bbnum = 0
for _, row in df.iterrows():
    bbnum += 1
    print(row)
    print()
    extract_bb(row, bbnum, mobs_dir)



#def display_bb(path_to_image_file, xtl, ytl, xbr, ybr):
#    img = cv2.imread(path_to_image_file)
#    frame_width, frame_height, _ = img.shape
#    cv2.rectangle(img, (int(xtl*frame_width), int(ytl*frame_height)), (int(xbr*frame_width), int(ybr*frame_height)), (0, 255, 0), 3)
#    cv2.imshow(path_to_image_file, img)
#    cv2.waitKey(100)

#start = time.process_time()
#display_bb('bees.h264_frames/f009233.jpg', 0.50625, 0.9555555555555556, 0.5645833333333333, 1.0)
#print(time.process_time() - start)
    
#df = pd.DataFrame([{'filename': 'bees.h264_frames/f009222.jpg', 'xtl': 0.464583, 'ytl': 0.492593, 'xbr': 0.518750, 'ybr': 0.570370},
#                   {'filename': 'bees.h264_frames/f009222.jpg', 'xtl': 0.372917, 'ytl': 0.403704, 'xbr': 0.404167, 'ybr': 0.455556}])
#
## Load image in memory
#img = cv2.imread(df['filename'][0])
#
## Convert coordinates from proportions to pixels
#img_width, img_height, _ = img.shape
#df['xtl'] = df['xtl'].apply(lambda x: int(x * img_width))
#df['ytl'] = df['ytl'].apply(lambda x: int(x * img_height))
#df['xbr'] = df['xbr'].apply(lambda x: int(x * img_width))
#df['ybr'] = df['ybr'].apply(lambda x: int(x * img_height))
#
## Draw bounding boxes on image and display it.
#for _, row in df.iterrows():
#    cv2.rectangle(img, (row.xtl, row.ytl), (row.xbr, row.ybr), (0, 255, 0), 3)
##cv2.imshow(row.filename, img)
##cv2.waitKey(1000) & 0xFF
#filename = '{}/f{:0>6}.jpg'.format(outdir, framenum)
#cv2.imwrite(filename, original_frame)
#
## MAIN
#
#
