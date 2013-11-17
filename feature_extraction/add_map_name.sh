#!/bin/bash

head -n 1 $1 | sed 's/^/map,/' > $2
tail -n +2 $1 | sed 's/^/'$3',/' >> $2
