# -*- coding: utf-8 -*-
#!/usr/bin/python

from linebot import LineBotApi
from linebot.models import TextSendMessage
import time
import os
import re
import subprocess
from  line_messenger import pushMessage

pushMessage('U49f9b5ee8127f7fa2357935415ea379c','系統開機完成，網路連接成功！')
sentMessage = ''
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

# Check Mapillary credential
mapillaryConfig = open('/home/pi/.config/mapillary/config', 'r')
if len(mapillaryConfig.readlines()) == 0:
    pushMessage('U49f9b5ee8127f7fa2357935415ea379c','您尚未設定 Mapillary 帳號！使用終端機執行以下指令，並依序輸入：\n1. 您的 Mapillary 使用者代號。\n2. 您註冊 Mapillary 的 email。\n3. 您的 Mapillary 密碼。')
    pushMessage('U49f9b5ee8127f7fa2357935415ea379c','mapillary_tools authenticate --advanced')
    pushMessage('U49f9b5ee8127f7fa2357935415ea379c','* 如需重設密碼，請至： https://www.mapillary.com/app/?login=true')
    pushMessage('U49f9b5ee8127f7fa2357935415ea379c','* 如需申請帳號，請至： https://www.mapillary.com/app/?signup=true')
    pushMessage('U49f9b5ee8127f7fa2357935415ea379c','* 此工具不支援Facebook、Google、OpenStreetMap等登入方式。')
    pushMessage('U49f9b5ee8127f7fa2357935415ea379c','登入失敗，作業結束。')
    mapillaryConfig.close()
else:
    mapillaryConfig.close()
    # Scan mounted media
    while not memoryCardExisted:
        messageSearchMemoryCard = '請插入記憶卡。'
        if sentMessage != messageSearchMemoryCard:
            sentMessage = messageSearchMemoryCard
            pushMessage('U49f9b5ee8127f7fa2357935415ea379c', messageSearchMemoryCard)
        time.sleep(2)
        for dirPath, dirNames, fileNames in os.walk(rootPath):
            if not re.findall('/media/pi/SETTINGS', dirPath) and dirPath != '/media' and dirPath != '/media/pi':
                pushMessage('U49f9b5ee8127f7fa2357935415ea379c', '發現記憶卡，10秒後開始作業，請稍候。')
                time.sleep(10)
                memoryCardExisted = True
                break

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
            pushMessage('U49f9b5ee8127f7fa2357935415ea379c', '處理GPS軌跡資料。')
            pushMessage('U49f9b5ee8127f7fa2357935415ea379c', allTraceFileList)

        # print 'gpsbabel -i nmea{} -o gpx,gpxver=1.1 -F "{}"'.format(gpxMergeInput, mergedGpxFilePath)
        os.system('gpsbabel -i nmea{} -o gpx,gpxver=1.1 -F "{}"'.format(gpxMergeInput, mergedGpxFilePath))
        pushMessage('U49f9b5ee8127f7fa2357935415ea379c', 'GPS軌跡處理完畢，輸出檔案： {}'.format(mergedGpxFilePath))
        pushMessage('U49f9b5ee8127f7fa2357935415ea379c', '開始將影片檔轉換為JPG圖檔。')

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
        
        # Sample images from Video
        for videoSubDirPath in videoDirPath:
            pushMessage('U49f9b5ee8127f7fa2357935415ea379c', '處理影片資料夾：{}'.format(videoSubDirPath))
            # videoProcessCommand = '/home/pi/.local/bin/mapillary_tools video_process --rerun --import_path {} --video_import_path {} --user_name {} --advanced --geotag_source gpx --geotag_source_path {} --video_sample_interval 1 --interpolate_directions'.format(imageFolder, videoSubDirPath, mapillaryUserName, mergedGpxFilePath)
            videoProcessCommand = '/home/pi/.local/bin/mapillary_tools video_process_and_upload --rerun --import_path {} --video_import_path {} --user_name {} --advanced --geotag_source gpx --geotag_source_path {} --video_sample_interval 1 --interpolate_directions'.format(imageFolder, videoSubDirPath, mapillaryUserName, mergedGpxFilePath)
            videoProcessCommandList = videoProcessCommand.split(' ')
            p = subprocess.Popen(videoProcessCommandList, stdout=subprocess.PIPE, bufsize=1)
            p.wait()
        
        '''
        # Upload images to Mapillary
        sampledVideoFramesPath = os.path.join(imageFolder, 'mapillary_sampled_video_frames')
        mapillaryToolsLogPath = os.path.join(imageFolder, '.mapillary')
        pushMessage('U49f9b5ee8127f7fa2357935415ea379c', '影片轉換完成！開始上傳JPG圖檔至 Mapillary。')
        uploadCommand = '/home/pi/.local/bin/mapillary_tools upload --import_path "{}"'.format(imageFolder)
        os.system(uploadCommand)
        os.system("rm -rf {}".format(sampledVideoFramesPath))
        os.system("rm -rf {}".format(mapillaryToolsLogPath))
        '''
        
        for dir in allDirs:
            umountCommand = 'umount {}'.format(dir)
            os.system(umountCommand)
        
        pushMessage('U49f9b5ee8127f7fa2357935415ea379c', '上傳完畢，成功移除記憶卡。')
        
        '''
        pushMessage('U49f9b5ee8127f7fa2357935415ea379c', '系統將於 30 秒後關機。')
        time.sleep(30)
        pushMessage('U49f9b5ee8127f7fa2357935415ea379c', '系統關機')
        os.system('sudo shutdown -h')
        '''
