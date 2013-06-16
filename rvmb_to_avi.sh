#! /bin/bash

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
# Get all the files that end in rvmb into a list
for i in $(ls) ; do
    file=${i%.*}
    ext=${i#*.}
    echo $file
    echo $ext
    if [ "$ext" = "rmvb" ]; then
	mencoder $file.rmvb -oac mp3lame -lameopts preset=128 -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=1200 -ofps 25 -of avi -o $file.avi
	rm "$file.rmvb"
    fi;
done;
IFS=$SAVEIFS
# Loop through list

# convert the file
# remove the old file
