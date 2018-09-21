#!/usr/bin/env python
# coding: utf-8
import re
import time
from datetime import datetime

# In[2]:
#验证语句合法性
#必须包含时间信息：上午|下午|晚
def formatChecker(s):
    index= 0
    for sentence in s.sentences:
        check_pattern = re.compile(r'上午|下午|晚|明早')
        if (re.search(check_pattern, sentence)):
            print("baseSentence: " + sentence)
            return index
        index = index + 1
    return -1

#将字符串格式的时间 转化为时间格式
#dayStr : 今晚、晚上、明早
#timeStr : 7:10 等
#例：今晚7.10  =>  2018-09-20 19:10:00
def timeGenerator(dayStr,timeStr) :
    now = time.localtime(time.time())
    departure_time = now
    if ("明" in dayStr):
        tomorrow = time.localtime(time.time() + 86400)
        departure_time =  time.strftime('%Y-%m-%d', tomorrow)
    else:
        departure_time = time.strftime('%Y-%m-%d', now)
        
    time_pattern = re.compile(r'([012]?\d)([:.：点] ?)(\d{1,2})')
    print("timeStr: ",timeStr)
    timeStr = re.findall(time_pattern,timeStr)[0]
    
    if(timeStr[2] == ""):
        timeStr = "00"
    timeStr = timeStr[0] + ":" + timeStr[2] + ":" + "00"
    #得到time string
    departure_time = departure_time + " " + timeStr
    #转换成datetime
    departure_time = datetime.strptime(departure_time, "%Y-%m-%d %H:%M:%S")
    #转换成timetuple 用来判断是否为24小时模式
    departure_time = departure_time.timetuple()
    if("晚" in dayStr and departure_time.tm_hour < 12):
        #将时间转换为24小时形式
        departure_time = time.localtime(time.mktime(departure_time) + 43200)
        
    departure_time = time.strftime('%Y-%m-%d %H:%M:%S', departure_time)
    return departure_time

test = timeGenerator("明早","7：10")

print(test)

#以-－～~——一符号连接，连续两个以上的
def getRoute(sentences,index):
    route_pattern = re.compile(r'\w{0,5}([-－～~——一]\w{2,8}){2,10}')
    while(index < len(sentences)):
        route = route_pattern.search(sentences[index])
        if(route):
            return route.group()
        else:
            index = index + 1
    else:
        return ""

#写入小括号中的内容将解析在description 字段
def getDescription(msg):
    description = ""
    description_pattern = re.compile(r'[\(（](.*?)[\)）]')
    resultArray = re.findall(description_pattern,msg)
    for i in resultArray:
        description = description + i + " "
    return description


#得到
def getOrigin(dayStr, route, msg, baseSentence):
    if("早" in dayStr):
        if("出发" in baseSentence):
            origin_pattern = re.compile(r'\w{3,4}出发')
            origin = origin_pattern.search(msg)
            return origin.group()
        elif(len(route) > 0):
            origin_pattern = re.compile(r'(\w{0,5})[-－～~——一]')
            origin = origin_pattern.findall(route)[0]
            if("出发" in origin):
                return origin
            else:
                return origin + "出发"
        else:
            return "廊坊出发"

    else:
        origin_pattern = re.compile(r'(分钟寺|十里河)[a-zA-Z]?(口|出口)?')
        origin = re.search(origin_pattern,msg)
        return origin.group()