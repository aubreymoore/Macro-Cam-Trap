#!/bin/bash
#
# trapcam.sh
#
# Aubrey Moore (aubreymoore@guam.net) 2019-07-17
#
# This bash script is intended for runnung only on a Raspberry Pi 
# equiped with a camera.
#################################################################

# Check for  USB storage device; exit if not found
##################################################
if [ -z "$(ls -A /media/pi)" ]
then
    echo "ERROR: Cannot find USB memory for data storage at /media/pi."
    echo "Abnormal termination"
    exit
else
    datadir="/media/pi/$(ls /media/pi)" 
    echo "Data will be stored on $datadir"
    df -h $datadir
    echo
fi

# Make a "videos" directory on the storage device if it does not already exist
##############################################################################

videodir=${datadir}/videos
mkdir -p $videodir

# Check for configuration file in top level directory of USB storage device.
############################################################################

file="${datadir}/macrocamtrap.config"
if [ -f "$file" ]
then
    echo "$file found"
    # Copy macrocamtrap.config from USB storage device to the same directory
    # as this script
    echo "Copying macrocamtrap.config from USB memory device to RPi"
    cp $file macrocamtrap.config 
else
    echo "$file not found"
    # Copy macrocamtrap.config from same directory as this script to top level
    # directory of the USB storage device
    echo "Copying from RPi to USB memory device"
    echo cp macrocamtrap.config $file
    cp macrocamtrap.config $file
fi

# Read parameters from conf file
################################

source macrocamtrap.config


########################################
# RECORD AND (OPTIONALLY) PROCESS VIDEOS
########################################

for ((i = 1 ; i<= $MAX_VIDEOS ; i++))
do

   # Record video using raspivid
   #############################
   
   # Get timestamp for start of video in ms since epoch

   timestamp=$(date +%s%3N)

   mkdir -p ${videodir}/$timestamp
   video_file_name=${videodir}/${timestamp}/${timestamp}.h264
   echo
   echo raspivid -o $video_file_name -t $VIDEO_LENGTH_MS -p $PREVIEW_WINDOW
   raspivid -o $video_file_name -t $VIDEO_LENGTH_MS -p $PREVIEW_WINDOW

   # Store a copy of macrocamtrap.config in same directory as video and frames
   cp macrocamtrap.config ${videodir}/${timestamp}/macrocamtrap.config

   # Process video
   ###############

   if [ "$PROCESS_VIDEO" = true ] ; then
      echo python3 motion_detector.py $videodir $timestamp  
      python3 motion_detector.py $videodir $timestamp  
      if [ "$DELETE_VIDEO_AFTER_PROCESSING" = true ] ; then
         echo "   Deleting video."
         rm $video_file_name
      fi
   fi

   # Display remaining memory for output data

   df $datadir -h
   echo
done

echo
echo "Normal termination"
