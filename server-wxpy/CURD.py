#!/usr/bin/env python
# coding: utf-8

from transform import *
import pymysql

def insertRoute(db,msg):

    sql = transformToSql(msg)

    # In[8]:
    try:
        # 执行sql语句
        cursor = db.cursor()
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
        print("SUCCESS")
        return True
    except:
        print("ERROR")
        return False

