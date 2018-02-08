#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import json
import time
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

db = ''
cursor = ''


def parseData():
    initDB();
    file_object = open('info.txt')
    text = file_object.readline()
    while text:
        print(text)
        dic = json.loads(text)
        
        timeStru = time.strptime(dic['deviceDate'],'%Y/%m/%d %H:%M')
        deviceDate = time.strftime('%Y/%m/%d %H:%M:%S',timeStru)
        timeStru = time.strptime(dic['createDate'],'%Y/%m/%d %H:%M')
        createDate = time.strftime('%Y/%m/%d %H:%M:%S',timeStru)
        
        sql = 'replace into %s values(%s,%s,%s,%s,%s,%s) ' % ('warnings',dic['id'],"'"+dic['name']+"'","'"+dic['model']+"'","'"+dic['warn']+"'","'"+deviceDate+"'","'"+createDate+"'")
        executeSQL(sql)
        text = file_object.readline()

    closeDB()

def initDB():
    global db
    global cursor
    db = MySQLdb.connect(host="localhost",user="root",passwd="216567",db="gps_db",use_unicode=True,charset="utf8")
    cursor = db.cursor()

def closeDB():
    global db
    db.close()

def executeSQL(sql):
    global db
    global cursor
    print("the sql is:"+sql)
    print("executeSQL")
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()


