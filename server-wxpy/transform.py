#!/usr/bin/env python
# coding: utf-8

# In[1]:
import re
from common import *
from snownlp import SnowNLP


def transformToSql(msg):
    sql = ""
    s = SnowNLP(msg)
    sentences = s.sentences

    # In[3]:
    baseSentence = formatChecker(s)
    if( baseSentence == None or len(baseSentence) == 0):
        print("格式错误")
        return ""

    day_pattern =  re.compile(r'今晚|晚上|明早')   
    #tomorning_pattern = re.compile(r'明早')
    time_pattern = re.compile(r'[012]?\d[:.：点] ?\d{1,2}')
    origin_pattern = re.compile(r'(分钟寺|十里河)[a-zA-Z]?(口|出口)?')
    telephone_pattern = re.compile(r'1[3-9][0-9]{9}')
    seats_pattern = re.compile(r'(空[一-六两])|([一-六两]位)')

    if("终点" in msg):
        destination_pattern = re.compile(r'(终点|回)(\w{3,4})')
    else:
        # route 要以 - 或者 ～ 连接 以中文句号。 或者空格结尾
        destination_pattern = re.compile(r'(-|～)(\w{3,4})($|。| )')
    
    dayStr = day_pattern.findall(baseSentence)
    #print(dayStr)
    gatherTime = time_pattern.findall(baseSentence)
    if(len(gatherTime) == 0):
        time_pattern_2 = re.compile(r'[012]?\d[点]')
        gatherTime = time_pattern_2.findall(baseSentence)
        gatherTime[0] = gatherTime[0] + "00" 
    else:
        print("格式错误")
        return ""

    origin = re.search(origin_pattern,msg)
    if(origin == None):
        print("格式错误")
        return ""
    telephone = re.findall(telephone_pattern,msg)
    route = sentences[1]

    try:
        destination = re.findall(destination_pattern,msg)[0][1]
    except :
        print("未找到Destination,取默认值")
        #晚上出发取廊坊，早上出发取北京
        if("晚" in dayStr):
            destination = "廊坊"
        else:
            destination = "北京"
        pass
    
    try:
        seats = re.findall(seats_pattern,msg)[0][0]
    except :
        seats = ""
        pass
    

    # In[4]:

    publisher = '李永楠test'
    #print(dayStr)
    #print(gatherTime[0])
    departure_time = timeGenerator(dayStr[0],gatherTime[0])
    departure_time_info = dayStr[0] + gatherTime[0]
    direction = 1
    origin = origin.group()
    destination = destination
    route = route
    seats = seats
    car_id = ''
    telephone = telephone[0]
    message = msg
    description = ''

    # In[5]:

    sql = " INSERT INTO `aipin`.`aipin_route` ( `publisher`, `departure_time`, `departure_time_info`, `direction`, `origin`, `destination`, `route`, `seats`, `car_id`, `telephone`, `message`, `description`) VALUES ('%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" % (publisher, departure_time, departure_time_info, direction, origin, destination, route, seats, car_id,telephone,message,description)
    print(sql)

    return sql

def formatChecker(s):
    baseSentence = ""
    for sentence in s.sentences:
        check_pattern = re.compile(r'上午|下午|晚')
        if (re.search(check_pattern, sentence)):
            baseSentence = sentence
            print("baseSentence: " + baseSentence)
            return baseSentence

