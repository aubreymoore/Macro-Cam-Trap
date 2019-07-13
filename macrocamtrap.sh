#!/bin/bash
#
# trapcam.sh
#
# Aubrey Moore 2019-07-13
#

# Check for  USB storage device; exit if not found

if [ -z "$(ls -A /media/pi)" ]
then
   echo "ERROR: Cannot find USB memory for data storage."
   exit
else
   data_dir="/media/pi/$(ls /media/pi)" 
   echo "Data will be stored on $data_dir"
   df -h $data_dir
fi

# Read parameters from conf file

source macrocamtrap.config

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
   echo raspivid -o $video_file_name -t $VIDEO_LENGTH_MS -p $PREVIEW_WINDOW
   raspivid -o $video_file_name -t $VIDEO_LENGTH_MS -p $PREVIEW_WINDOW

   # Process video

   if [ "$PROCESS_VIDEO" = true ] ; then
      echo python3 motion_detector.py $VIDEO_DIR $timestamp  
      python3 motion_detector.py $VIDEO_DIR $timestamp  
      if [ "$DELETE_VIDEO_AFTER_PROCESSING" = true ] ; then
         echo "   Deleting video."
         rm $video_file_name
      fi
   fi

   # Display remaining memory for output data

   df $VIDEO_DIR -h
   echo
done

