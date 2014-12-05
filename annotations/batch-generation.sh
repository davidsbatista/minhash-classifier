#!/bin/bash

STANDOFF2INLINE=../../../standoff2inline.py

for i in *.txt; 
do 
    FILE=`basename $i .txt`;
    PWD=`pwd`
    DIR=`basename $PWD`
    $STANDOFF2INLINE $i $FILE.'ann' > $FILE.inline
done
