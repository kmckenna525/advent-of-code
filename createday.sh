#!/bin/bash
if [ -z $1 ]; then
	echo "Provide day or year and day as parameters"
	exit 1
fi

year=$1
day=$2
if [ -z $2 ]; then
	year=2020
	day=$1
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

