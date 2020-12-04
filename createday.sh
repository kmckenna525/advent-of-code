#!/bin/bash
year=$1
day=$2
if [ -z $2 ]; then
	year=2020
	day=$1
fi

dir=$year/day$day

if [ -d $dir ]; then
	echo "$dir already exists"
	exit 0
fi

cp -r template $dir
sed -i "" "s/# Day/# $year Day $day/" $dir/notes.md

echo "Created $dir"
