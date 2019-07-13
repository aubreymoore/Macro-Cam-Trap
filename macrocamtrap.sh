#!/bin/bash
#
# trapcam.sh
#
# Aubrey Moore 2019-07-11
#

workon cv

# Read parameters from conf file
source trapcam.config

# Make a directory for videos if it does not already exist
mkdir -p $VIDEO_DIR

for ((i = 1 ; i<= $MAX_VIDEOS ; i++))
do

   # Record video

   # Get timestamp for start of video in ms since epoch
   timestamp=$(date +%s%3N)

   mkdir -p ${VIDEO_DIR}/$timestamp
   video_file_name=${VIDEO_DIR}/${timestamp}/${timestamp}.h264
   echo "recording $video_file_name [ CTRL+C to stop ]"
   raspivid -o $video_file_name -t $VIDEO_LENGTH_MS -p $PREVIEW_WINDOW

   # Process video

   if [ "$PROCESS_VIDEO" = true ] ; then
       python2 motion_detector.py $VIDEO_DIR/${timestamp} $video_file_name    
       echo "   Processing video."
      if [ "$DELETE_VIDEO_AFTER_PROCESSING" = true ] ; then
         echo "   Deleting video."
         rm $video_file_name
      fi
   fi

   # Display remaining memory for output data

   df $VIDEO_DIR -h
   echo
done

