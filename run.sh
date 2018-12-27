#!/bin/bash
#run.sh

# cd /home/pi/Mapiberry/
python /home/pi/Mapiberry/cpu_temp.py &
python /home/pi/Mapiberry/log_checker.py &
python /home/pi/Mapiberry/main.py > /home/pi/Mapiberry/log.txt 2>&1