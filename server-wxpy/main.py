#!/usr/bin/env python
# coding: utf-8
from CURD import *

# 打开数据库连接
db = pymysql.connect("localhost","lyn","lyn","aipin" )

#1. 打开文件，得到文件句柄并赋值给一个变量
f=open('testData.txt',encoding='utf-8') #默认打开模式就为r
list = []
#2. 通过句柄对文件进行操作
lineNum = 0
for line in f:
    print(line)
    lineNum = lineNum + 1
    if insertRoute(db,line):
       pass
    else:
        list.append(line)

print("ERROE LISTS: ", list)
print("识别率: ",   (1 - len(list) / lineNum)*100, "%")
#3. 关闭文件
f.close()
#关闭数据库

db.close()