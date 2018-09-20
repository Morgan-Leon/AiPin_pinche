#!/usr/bin/env python
# coding: utf-8
import re
import time
from datetime import datetime

# In[2]:


#将字符串格式的时间 转化位时间格式
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