#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import sys
import os
import xml.dom.minidom
import json
import time
import shutil
import dataParse
reload(sys)
sys.setdefaultencoding('utf-8')

data_backup_dir = 'data_backups/warnings/'
if not os.path.isdir(data_backup_dir):
    os.mkdir(data_backup_dir)

def backup_data():
    t = time.localtime()
    ts = time.strftime('%y-%m-%d_%H:%M:%S',t)
    if not os.path.isdir(data_backup_dir):
        os.mkdir(data_backup_dir)
    shutil.copy('info.txt', '{}{}.txt'.format(data_backup_dir, ts))

def fetchData():
    file_object = open('info.txt', 'w')

    headers = {'User-Agent':'boorgeel/1 CFNetwork/811.5.4 Darwin/16.7.0','SOAPAction':'http://tempuri.org/GetWarnList','Accept-Language':'zh-cn','Content-Type':'text/xml; charset=utf-8'}
    body = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><GetWarnList xmlns="http://tempuri.org/"><ID>23166</ID><PageNo>1</PageNo><PageCount>30</PageCount><TypeID>1</TypeID><TimeZones>China Standard Time</TimeZones><Language>zh-Hans-CN</Language><Key>7DU2DJFDR8321</Key></GetWarnList></soap:Body></soap:Envelope>'
    
    r = requests.post("http://app.boorgeel.com:9911/openapiv3.asmx", headers = headers, data = body)

    DOMTree = xml.dom.minidom.parseString(r.text)
    collection = DOMTree.documentElement
#    print(collection.getElementsByTagName('GetWarnListResult')[0].firstChild.data)
    rawData = collection.getElementsByTagName('GetWarnListResult')[0].firstChild.data
    dataDic  = json.loads(rawData)
#    print(collection.getElementsByTagName('GetWarnListResult')[0].firstChild.data)
    print(dataDic)

    for item in dataDic['arr'] :
        text = json.dumps(item,ensure_ascii = False,encoding='utf-8')
        file_object.write(text+"\r\n")
        print(text)
    
    file_object.close()
#    解析数据并存储在mysql中
    dataParse.parseData()
    backup_data()
