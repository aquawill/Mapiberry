# -*- coding: utf-8 -*-

from linebot import LineBotApi
from linebot.models import TextSendMessage
import time
import os
import re
import subprocess


line_bot_api = LineBotApi('MgXDbs7VLmkhQ/7KJsP9280yct33lfXYylQs3wKKZHKkZ3BYjvgSZd1axKmTR1Ir6hIx0CnpFyO4j9KeoZ8zZDMEiapuNgkusME3gd0GrmANajlO2C/dCqVK870fnOUB08AamQUn9N5WBxaJIJtKlwdB04t89/1O/w1cDnyilFU=')

def addingTimestamp(text):
    timestamp = time.strftime("%d %b %Y %H:%M:%S", time.localtime(time.time()))
    return '{}\n{}'.format(timestamp, text)

def push_message(id, message):
    while True:
        try:
            line_bot_api.push_message(id, TextSendMessage(text=addingTimestamp(message)))
            break
        except Exception:
            print Exception.with_traceback
            print "Connection failure, retrying in 5 secs..."
            time.sleep(2)
            pass
        
def execute(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Poll process for new output until finished
    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() is not None:
            break
        sys.stdout.write(nextline)
        sys.stdout.flush()

    output = process.communicate()[0]
    exitCode = process.returncode

    if (exitCode == 0):
        return output
    else:
        raise ProcessException(command, exitCode, output)

push_message('U49f9b5ee8127f7fa2357935415ea379c','系統開機完成，網路連接成功！')
memoryCardExisted = False
mapillaryUserName = 'aquawill'
videoDirPath = set()
rootPath = '/media'
gpxMergeInput = ''
mergedGpxFilePath = ''
imageFolder = ''
allTraceFileList = ''
allVideoFileList = ''
allDirs = []

# Scanning
while not memoryCardExisted:
    time.sleep(2)
    for dirPath, dirNames, fileNames in os.walk(rootPath):
        if not re.findall('/media/pi/SETTINGS', dirPath) and dirPath != '/media' and dirPath != '/media/pi':
            push_message('U49f9b5ee8127f7fa2357935415ea379c', '發現記憶卡，掃描中‥‥‥')
            memoryCardExisted = True
            break
    print addingTimestamp('no memory card mounted.')

if memoryCardExisted:
    for dirPath, dirNames, fileNames in os.walk(rootPath):
        try:
            if not re.findall('/media/pi/SETTINGS', dirPath) and dirPath != '/media' and dirPath != '/media/pi':
                allDirs.append(dirPath)
                for fileName in fileNames:
                    fileBaseName, fileExt = os.path.splitext(fileName)
                    if fileExt.upper() == ".NMEA":
                        nmeaFilePath = os.path.join(dirPath, fileName)
                        allTraceFileList += '{}\n'.format(fileName)
                        gpxFilePath = os.path.join(dirPath, fileBaseName + '.GPX')
                        gpxMergeInput += ' -f "{}"'.format(nmeaFilePath)
                        mergedGpxFilePath = os.path.join(os.path.dirname(dirPath), 'merged.GPX')
        except Exception as e:
            pass
    print allDirs
    if len(allTraceFileList) > 0:
        push_message('U49f9b5ee8127f7fa2357935415ea379c', '處理GPS軌跡資料‥‥‥')
        push_message('U49f9b5ee8127f7fa2357935415ea379c', allTraceFileList)

    # print 'gpsbabel -i nmea{} -o gpx,gpxver=1.1 -F "{}"'.format(gpxMergeInput, mergedGpxFilePath)
    os.system('gpsbabel -i nmea{} -o gpx,gpxver=1.1 -F "{}"'.format(gpxMergeInput, mergedGpxFilePath))
    push_message('U49f9b5ee8127f7fa2357935415ea379c', 'GPS軌跡處理完畢，輸出檔案： {}'.format(mergedGpxFilePath))
    push_message('U49f9b5ee8127f7fa2357935415ea379c', '開始將影片檔轉換為JPG圖檔‥‥‥')

    for dirPath, dirNames, fileNames in os.walk(rootPath):
        for fileName in fileNames:
            fileBaseName, fileExt = os.path.splitext(fileName)
            if fileExt.upper() == ".MP4":
                # mp4FilePath = os.path.join(dirPath, fileBaseName + ".MP4")
                # gpxFilePathByVideo = os.path.join(dirPath, fileBaseName + ".GPX")
                imageFolder = os.path.dirname(dirPath)
                memoryCardPath = os.path.dirname(imageFolder)
                if dirPath[-1] != "R":
                    videoDirPath.add(dirPath)
                    
    # Mapillary Uploader
    for videoSubDirPath in videoDirPath:
        # print 'mapillary_tools video_process_and_upload --rerun --import_path "{}" --video_import_path "{}" --user_name "{}" --advanced --geotag_source "gpx" --geotag_source_path "{}" --video_sample_interval 1 --interpolate_directions'.format(imageFolder, videoSubDirPath, mapillaryUserName, mergedGpxFilePath)
        push_message('U49f9b5ee8127f7fa2357935415ea379c', '處理影片資料夾：{}'.format(videoSubDirPath))
        c = 'mapillary_tools video_process --rerun --import_path "{}" --video_import_path "{}" --user_name "{}" --advanced --geotag_source "gpx" --geotag_source_path "{}" --video_sample_interval 1 --interpolate_directions'.format(imageFolder, videoSubDirPath, mapillaryUserName, mergedGpxFilePath)
        # subprocess.Popen([c], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
        os.system(c)
    
    sampledVideoFramesPath = os.path.join(imageFolder, 'mapillary_sampled_video_frames')
    mapillaryToolsLogPath = os.path.join(imageFolder, '.mapillary')
    push_message('U49f9b5ee8127f7fa2357935415ea379c', '影片轉換完成！輸出JPG圖檔至： {}'.format(sampledVideoFramesPath))
    push_message('U49f9b5ee8127f7fa2357935415ea379c', '開始上傳JPG圖檔至 Mapillary ‥‥‥')
    uploadCommand = 'mapillary_tools upload --import_path "{}"'.format(sampledVideoFramesPath)
    #out = subprocess.Popen([c], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    os.system(uploadCommand)
    os.system("rm -rf {}".format(sampledVideoFramesPath))
    os.system("rm -rf {}".format(mapillaryToolsLogPath))

    for dir in allDirs:
        umountCommand = 'umount {}'.format(dir)
        os.system(umountCommand)
    
    push_message('U49f9b5ee8127f7fa2357935415ea379c', '上傳完畢，成功移除記憶卡。')
    push_message('U49f9b5ee8127f7fa2357935415ea379c', '系統將於 30 秒後關機。')
    time.sleep(30)
    push_message('U49f9b5ee8127f7fa2357935415ea379c', '系統關機')
    os.system('sudo shutdown -h')

