#!/bin/bash

# SELF_NAME
SELF_INFO=$(ls|grep -m 1 .*.info)
SELF_NAME=$(sed -e '/SELF_NAME=/!d' -e 's/SELF_NAME=//g' $SELF_INFO)

# If SELF_NAME is empty then error exit
if [ "$SELF_NAME" == "" ]
then
	echo "$(date "+%Y-%m-%d %T") [ERROR] SELF_NAME is not defined in info file!"
	exit 0
fi 

# Make list of directories
dir_list=($(sed -e 's/SELF_.*=//g' -e '/^\//!d' -e "s/$SELF_NAME\/$SELF_NAME.*/$SELF_NAME\//g" $SELF_INFO))

# Make directories in list
for dir in ${dir_list[@]}
do 	if [ ! -f $dir ]
	then 	mkdir -p $dir
		echo "$(date "+%Y-%m-%d %T") [INFO] $dir has been created"
	fi
done
