#!/bin/bash

PATHTOWEKAJAR=/home/douglas/programs/weka-3-6-10/weka.jar

java -Xmx2G -cp $PATHTOWEKAJAR weka.classifiers.trees.J48 -t $1 -c $2

