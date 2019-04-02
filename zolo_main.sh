#!/bin/bash

project1='zolo_main.py'


for Pro in $project1

do

PythonPid=`ps -ef | grep $Pro | grep -v grep | wc -l `

echo $Pro
if [ $PythonPid -eq 0 ];
        then
        echo "`date "+%Y-%m-%d %H:%M:%S"`:$Pro is not running" >> /realtor/logs/python.log

        cd /data/project/AmericaSpiderClientServer/
        
        nohup python3 $Pro > nohup.out 2>&1 &

        echo "`date "+%Y-%m-%d %H:%M:%S"`:$Pro is starting" >> /realtor/logs/python.log
        sleep 5
        CurrentPythonPid=`ps -ef | grep $Pro | grep -v grep | wc -l`
        if [ $CurrentPythonPid -ne 0 ];
        then
        echo "`date "+%Y-%m-%d %H:%M:%S"`:$Pro is running" >> /usr/project/logs/python.log
        fi
fi
done
