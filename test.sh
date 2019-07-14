#!/bin/sh

# Source macrocamtrap.config from the copy on RPi

source ~/macrocameratrap/macrotrapcam.config
echo $VIDEO_LENGTH

# Check for  USB storage device; exit if not found

if [ -z "$(ls -A /media/pi)" ]
then
    echo "ERROR: Cannot find USB memory for data storage."
    echo "Abnormal termination"
    exit
else
    datadir="/media/pi/$(ls /media/pi)" 
    echo "Data will be stored on $datadir"
    df -h $datadir
    echo
fi

# Make a "videos" directory on the storage device if it does not already exist
videodir=${datadir}/videos
mkdir -p $videodir

# Check for configuration file in top level directory of USB storage device.

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


echo
echo "Normal termination"
