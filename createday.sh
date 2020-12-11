#!/bin/bash
if [ -z $1 ]; then
	echo "Provide day or year and day as parameters"
	exit 1
fi

re='^[0-9]+$'
if ! [[ $1 =~ $re ]] ; then
   echo "error: $1 should be numeric"
   exit 1
fi
if ! [ -z $2 ] && ! [[ $2 =~ $re ]] ; then
   echo "error: $2 should be numeric"
   exit 1
fi

year=$1
day=$2
if [ -z $2 ]; then
	year=2020
	day=$1
fi

if [ $day -gt 25 ]; then
   echo "error: day should be max 25"
   exit 1
fi

if [ ${#day} -eq 1 ]; then
	day="0$day"
fi

dir=$year/day$day

if [ -d $dir ]; then
	echo "$dir already exists"
else
	cp -r template $dir
	sed -i "" "s/# Day/# $year Day $day/" $dir/notes.md

	echo "Created $dir"
fi

echo "cd $dir"

