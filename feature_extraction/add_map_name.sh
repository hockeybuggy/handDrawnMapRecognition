#!/bin/bash

TEMP=intermid.csv

head -n 1 $1 | sed 's/^/map,/' > $TEMP
tail -n +2 $1 | sed 's/^/'$3',/' >> $TEMP

sed 's/^\([^,]*\),\([^,]*\),\([^,]*\),\(.*\)/\2,\3,\1,\4/g' $TEMP > $2
