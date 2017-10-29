#!/usr/bin/env bash

RC=1

echo $continue
while [ $RC == 1 ]
do
    echo "Alter Ego starting..."
    ./alter_ego.py
    RC=$?
done

