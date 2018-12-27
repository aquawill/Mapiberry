# -*- coding: utf-8 -*-
#!/usr/bin/python

import time
import os
from line_messenger import pushMessage

overheat = False

def measureTemp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return float(temp.replace("temp=","").replace("'C", "").replace('\n', ''))

while True:
    t = measureTemp()
    if t > 79.9:
        overheat = True
    else:
        overheat = False
    if not overheat:
        time.sleep(5)
    else:
        pushMessage('U49f9b5ee8127f7fa2357935415ea379c', 'CPU溫度警告： {} 度！\n60秒後重新測量'.format(t))
        time.sleep(60)
