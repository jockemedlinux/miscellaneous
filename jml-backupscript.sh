#!/bin/bash
##@JOCKEMEDLINUX BACKUP-SCRIPT 2023-08-13##

##THIS SCRIPT PROVIDES A .IMG FILE YOU CAN###
##FLASH ONTO YOUR HD SD-CARD, USB ETC USING##
##TOOLS LIKE BALENA-ETCHER##

### DEVICES AND FILESYSTEMS
backupdevice=/dev/sda
backupdirectory=/mnt/DATADISK/_BACKUPS/server/thinker-server
name=thinker_
fileoutput=$name$(hostname)_$(date +%F).img

### LOOP DEVICES
loop=/dev/loop0
loopdev=/dev/loop0p2

### LOG FILE. WILL BE PLACED IN CURRENT DIRECTORY.
log_file="./$(date +%F)_backupscript.log"

### FUNCTION TO PRINT ERROR AND EXIT
abort() {
    echo -e "\e[91m[ERROR] $1\e[0m"
    echo -e "\e[91m[ERROR] Removing loopdevices and restoring services and dockers\e[0m"
    sleep 5
    docker start $(docker ps -a -q)
    losetup -D
    exit 1
}

### CHECKPOINT FUNCTION
checkpoint() {
    if [ $? -ne 0 ]; then
        abort "An error occurred during: [$1]"
    fi
    echo -e "\e[92m[+] [PASSED]: $1\e[0m\n[-------------------------------------------------------------------------------------------]"
    ## UNCOMMENT TO SLOW DOWN SCRIPT.
    # sleep 5
}

####################################################################################
echo -e "####################################################################################"
echo -e '\e[93mRun script like "./backup-script.sh | tee `date +%F`.log" for logging.\e[0m'
echo -e "####################################################################################\n"

### CHECK SUDO RIGHTS
if [ $EUID != 0 ]; then
    echo -e "\n\e[91m[ERROR] Please run this script with sudo permissions\e[0m\n"
    exit 1
fi
checkpoint "Sudo permissions used"

### NEEDED PACKAGES
packages="pv e2fsck dumpe2fs resize2fs truncate docker losetup smbd"
echo -e "\e[93m[INFO] Checking needed packages and programs\e[0m\n"
for line in $packages; do
    if which $line >/dev/null; then
        echo -e "\e[92m[+] $line: \t is installed\e[0m"
    else
        echo -e "\e[91m[ERROR] $line is not installed\e[0m"
        abort "Packages are missing"
    fi
done
echo -e ""
checkpoint "Found all needed settings and programs"

### STOP SERVICES AND DOCKERS
echo -e "\e[93m[INFO] Stopping services and dockers\e[0m"
docker stop $(docker ps -a -q)
checkpoint "Stopping services and dockers"

### CHECK BACKUP-FILE BEFORE BACKUP DEVICE
if [[ -e "$backupdirectory/$fileoutput" ]]; then
    echo -e "\e[93m[INSPECT] Backup-file already exists. Do you want to overwrite this file? [Y/N]: \e[0m"
    read answer
    if [[ $answer == "Y" || $answer == "y" ]]; then
        echo -e "\e[93m[INFO] Overwriting existing backup file...\e[0m"
        pv -tpreb $backupdevice | dd of=$backupdirectory/$fileoutput bs=1M conv=noerror,sparse
        checkpoint "Backing up device"
    else
        echo -e "\e[93m[INFO] Skipping backup.\e[0m"
        checkpoint "Skipping backup"
    fi
else
	echo -e "\e[93m[INFO] Overwriting existing backup file...\e[0m"
	pv -tpreb $backupdevice | dd of=$backupdirectory/$fileoutput bs=1M conv=noerror,sparse
	checkpoint "Backing up device"
fi

### FIND ORIGINAL FILESIZE
echo -e "\e[93m[INFO] Checking filesize\e[0m"
findsize=$(ls $backupdirectory/$fileoutput -lhS | awk '{print $5}')
if [[ -z $findsize ]]; then
	abort "File not found $1"
fi
echo -e "\tFilesize: $findsize"
checkpoint "Find original filesize"

### LOOP AND MINIMIZE DEVICE FILESYSTEM
sleep 5
echo -e "\e[93m[INFO] Check filesystem #1\e[0m"
losetup -f -P $backupdirectory/$fileoutput
sleep 5
e2fsck -pv $loopdev
checkpoint "Check filesystem #1"

### GATHER necessary INFO
echo -e "\e[93m[INFO] Gathering necessary information\e[0m"
blocksize=`dumpe2fs -h $loopdev | grep "Block size:" | awk '{print $3}'`
minsize=`resize2fs -P $loopdev | grep -o "[0-9]\+"`
start=`fdisk -lu | grep $loopdev | awk '{print $2}'`
startsize=`expr $start + 100`
minsizeconv=`expr $minsize \* 4096 / 512`
partend=`expr $startsize + $minsizeconv`
truncsize=`expr $partend \* 512`

echo -e "\n\e[93m[INFO] r2fs blocksize:\t\t$blocksize\t\t[4K blocks]\e[0m"
echo -e "\e[93m[INFO] r2fs minsize:\t\t$minsize\t\t[4K blocks]\e[0m"
echo -e "\e[93m[INFO] Start Sectors:\t\t$start\t\t[512 blocks]\e[0m"
echo -e "\e[93m[INFO] Start Sectors(+1):\t$startsize\t\t[51./2 blocks]\e[0m"
echo -e "\e[93m[INFO] Minsize Converted:\t$minsizeconv\t[512 blocks]\e[0m"
echo -e "\e[93m[INFO] Partition new end:\t$partend\t[512 blocks]\e[0m"
echo -e "\e[93m[INFO] Truncsize:\t\t$truncsize\t[bytes]\e[0m\n"
checkpoint "Gathering necessary informations"

############################################################################################
### DEBUG SECTION. UNCOMMENT TO STOP SCRIPT HERE BEFORE IRREVOCABLY TRUNCATE/RESIZE BACKUP FILE
#echo -e "\e[93m\n\nExiting script for improvements\n\n\e[0m"
#losetup -D
#exit 0
############################################################################################

### RESIZE FILESYSTEM TO MINIMUM SIZE
echo -e "\e[93m[INFO] Rezising filesystem. (The rest will be unallocated)\e[0m"
resize2fs -Mfp "$loopdev"
checkpoint "Resizing filesystem"

### CREATE NEW PARTITION SIZE ACCORDINGLY
echo -e "\e[93m[INFO] Creating the new partition\e[0m"
echo -e 'd\n2\nn\np\n2\n\n'$partend'\nw' | fdisk $loop 
checkpoint "Create the new partition"

### TRUNCATE THE IMAGE FILE TO SMALLEST POSSIBLE SIZE.
echo -e "\e[93m[INFO] Truncating image file\e[0m"
truncate --size=$truncsize $backupdirectory/$fileoutput
checkpoint "Truncating image file"

### RECHECK FILESYSTEM AFTER TRUNCATION.
echo -e "\e[93m[INFO] Check the filesystem #2\e[0m"
e2fsck -pv $loopdev
checkpoint "Check filesystem #2"

### FIND NEW FILESIZE
echo -e "\e[93m[INFO] Checking filesize\e[0m"
findnewsize=$(ls $backupdirectory/$fileoutput -lhS | awk '{print $5}')
if [[ -z $findnewsize ]]; then
	abort "File not found: $1"
fi
echo -e "\t[INFO] Filesize: $findnewsize"
checkpoint "Find new filesize"

### STATUS AND OUTPUTS.
echo -e "\e[93m[INFO] Old filesize:\t$findsize\e[0m"
echo -e "\e[93m[INFO] New filesize:\t$findnewsize\e[0m"
checkpoint "Find filesizes"

### CLEANUP
echo -e "\e[93m[INFO] Cleaning up\e[0m\n"
losetup -D
echo -e "\e[93m[INFO] Restarting dockers and services\e[0m"
docker restart $(docker ps -a -q)
systemctl restart smbd
checkpoint "[+] Congratulation! The script finished successfully and services has been restored. BYE!"
exit 0