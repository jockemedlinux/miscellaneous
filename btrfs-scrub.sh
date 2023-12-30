#!/bin/bash

docker stop -t 0 $(docker ps -a -q)
systemctl stop smbd

btrfs scrub start /mnt/DATADISK
btrfs scrub start /mnt/SSD

DATADISK_TIME=$(btrfs scrub status /mnt/DATADISK | awk '/Time left/')
SSD_TIME=$(btrfs scrub status /mnt/SSD | awk '/Time left/')
ETAD=$(btrfs scrub status /mnt/DATADISK)
ETASSD=$(btrfs scrub status /mnt/SSD)


echo -e "The BTRFS-scrubbing has started!"
echo -e "DATADISK: $DATADISK_TIME" 
echo -e "SSD DISK: $SSD_TIME" | wall


while true; do
	DATADISK_TIME=$(btrfs scrub status /mnt/DATADISK | awk '/Time left/')
	SSD_TIME=$(btrfs scrub status /mnt/SSD | awk '/Time left/')

	echo -e "The BTRFS-scrubbing in progress"
	echo -e "DATADISK: $DATADISK_TIME"
	echo -e "SSD DISK: $SSD_TIME"
	sleep 10
	clear

	if [[ -z $DATADISK_TIME && -z $SSD_TIME ]]; then
		echo -e "SCRUB SEEMS FINISHED. \n"
		echo -e "\nDATADISK:"
        btrfs scrub status /mnt/DATADISK
        echo -e "\nSSD:"
        btrfs scrub status /mnt/SSD
		break
	fi
done

docker start $(docker ps -a -q)
systemctl start smbd
curl -d "HDD SCRUB COMPLETE!" 10.77.0.200:6677/BACKUPS
