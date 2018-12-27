# -*- coding: utf-8 -*-
#!/usr/bin/python

import re
import time
from line_messenger import pushMessage

sentLine = ''

while True:
    try:
        log = open('log.txt', 'r')
        lines = log.readlines()
        if len(lines) == 1:
            if len(lines[0].split('\n')) == 1:
                lines = lines[0].split('\r')
            else:
                lines = lines[0].split('\n')
        line = lines[-1]
        if line != sentLine:
            if re.search('Extracting video frames', line):
                progressPercentage = line.split('|')[0].replace('Extracting video frames:', '').strip()
                progressProcessed = line.split('|')[2].split('[')[0].strip()
                progressRemainingTime = line.split('<')[1].split(',')[0]
                pushMessage('U49f9b5ee8127f7fa2357935415ea379c', '影片處理進度：{}\n已完成：{}\n預計剩餘時間：{}'.format(progressPercentage, progressProcessed, progressRemainingTime))
                sentLine = line
            if re.search('Processing image import properties', line):
                totalImages = line.split('/')[1].split('[')[0].strip()
                pushMessage('U49f9b5ee8127f7fa2357935415ea379c', '影片處理完成，產生 {} 張影像檔。'.format(totalImages))
                pushMessage('U49f9b5ee8127f7fa2357935415ea379c', '準備上傳影像，如影像數量多可能花費較長時間。'.format(totalImages))
                sentLine = line
            if re.search('Reading image capture time', line):
                totalImages = line.split('/')[1].split('[')[0].strip()
                pushMessage('U49f9b5ee8127f7fa2357935415ea379c', '上傳準備中：讀取影像時間資訊。'.format(totalImages))
                sentLine = line
            if re.search('Inserting gps data into image EXIF', line):
                totalImages = line.split('/')[1].split('[')[0].strip()
                pushMessage('U49f9b5ee8127f7fa2357935415ea379c', '上傳準備中：寫入 GPS 定位至 EXIF 。'.format(totalImages))
                sentLine = line
            if re.search('Loading geotag points', line):
                totalImages = line.split('/')[1].split('[')[0].strip()
                pushMessage('U49f9b5ee8127f7fa2357935415ea379c', '上傳準備中：讀取地理點位資訊。'.format(totalImages))
                sentLine = line
            if re.search('Finalizing sequence process', line):
                totalImages = line.split('/')[1].split('[')[0].strip()
                pushMessage('U49f9b5ee8127f7fa2357935415ea379c', '上傳準備中：處理影像參數。'.format(totalImages))
                sentLine = line
            if re.search('Inserting mapillary image description in image EXIF', line):
                totalImages = line.split('/')[1].split('[')[0].strip()
                pushMessage('U49f9b5ee8127f7fa2357935415ea379c', '上傳準備中：寫入 Mapillary 描述資料。'.format(totalImages))
                sentLine = line
        log.close()
    except:
        pass
    time.sleep(1)
