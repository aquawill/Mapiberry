from linebot import LineBotApi
from linebot.models import TextSendMessage
import time

lineBotApi = LineBotApi('MgXDbs7VLmkhQ/7KJsP9280yct33lfXYylQs3wKKZHKkZ3BYjvgSZd1axKmTR1Ir6hIx0CnpFyO4j9KeoZ8zZDMEiapuNgkusME3gd0GrmANajlO2C/dCqVK870fnOUB08AamQUn9N5WBxaJIJtKlwdB04t89/1O/w1cDnyilFU=')

def addingTimestamp(text):
    timestamp = time.strftime("%d %b %Y %H:%M:%S", time.localtime(time.time()))
    return '{}\n{}'.format(timestamp, text)

def pushMessage(id, message):
    while True:
        try:
            lineBotApi.push_message(id, TextSendMessage(text=addingTimestamp(message)))
            break
        except Exception:
            time.sleep(2)
            pass