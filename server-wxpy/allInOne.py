import re
import time
from datetime import datetime
from wxpy import *
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost","lyn","lyn","aipin" )
msgQueue = []
list = []
#导入wxpy模块的全部内容
bot=Bot(cache_path=True, console_qr=True)
# 初始化机器人，电脑弹出二维码，用手机微信扫码登陆
bot.groups(update=True, contact_only=False)
#微信登陆后，更新微信群列表（包括未保存到通讯录的群）
my_groups=bot.groups().search('AiPin')
my_groups[0].update_group(members_details=True)
my_groups[1].update_group(members_details=True)
print(my_groups)
@bot.register(my_groups, except_self=False)
#注册消息响应事件，一旦收到铲屎群的消息，就执行下面的代码同步消息。机器人自己在群里发布的信息也进行同步。
def msgCollector(msg):    
    print(msg)
    def process():
        insertRoute(db,msg)

    process()

# def sync_my_groups(msg):
#     sync_message_in_groups(msg, my_groups,run_async=False)
#同步“铲屎官1群”和“铲屎官2群”的消息。包括文字、图片、视频、语音、文件、分享、普通表情、地图等。


#堵塞线程，让机器人保持运行 
bot.join()

def insertRoute(db,msg):
    print("insertRoute1")
    sql = transformToSql(msg)
    print("insertRoute2")
    # In[8]:
    try:
        # 执行sql语句
        cursor = db.cursor()
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
        print("SUCCESS\n")
        return True
    except:
        print("ERROR\n")
        return False

def transformToSql(msg):
    print("transformToSql")
    sql = ""
    #s = SnowNLP(msg)
    #sentences = s.sentences
    sentences = msg
    # In[3]:
    index = formatChecker(msg)
    if(index < 0 ):
      print("formatChecker格式错误 ： 无早晚时间信息") 
      return ""
    #baseSentence = sentences[index]
    baseSentence = msg

    day_pattern =  re.compile(r'今晚|晚上|明早')   
    #tomorning_pattern = re.compile(r'明早')
    time_pattern = re.compile(r'[012]?\d[:.：点] ?\d{1,2}')
    #origin_pattern = re.compile(r'(分钟寺|十里河)[a-zA-Z]?(口|出口)?')
    telephone_pattern = re.compile(r'1[3-9][0-9]{9}')
    seats_pattern = re.compile(r'(空[一-六两])|([一-六两]位)')

    dayStr = day_pattern.findall(baseSentence)
    #print(dayStr)
    gatherTime = time_pattern.findall(baseSentence)
    if(len(gatherTime) == 0):
        time_pattern_2 = re.compile(r'[012]?\d[点]')
        gatherTime = time_pattern_2.findall(baseSentence)
        if(len(gatherTime) != 0):
            gatherTime[0] = gatherTime[0] + "00" 
        else:
            print("gatherTime格式错误：集合时间格式错误")
            return ""


    try:
        telephone = re.findall(telephone_pattern,msg)[0]
    except:
        telephone = ""
        pass

    route = getRoute(sentences,index)
    #origin = getOrigin(dayStr[0],route,msg,baseSentence)
    #origin = re.search(origin_pattern,msg)
  
    try:
        origin = getOrigin(dayStr[0],route,msg,baseSentence)
    except:
        print("getOrigin：出发格式出错")
        return ""


    if("终点" in msg or "回" in msg):
        #取“终点” 或者 回 后面 三个或四个 中文字符
        destination_pattern = re.compile(r'(终点|回)(\w{3,4})')
    else:
        # route 要以 - 或者 ～ 连接 以中文句号。 或者空格结尾
        destination_pattern = re.compile(r'(-|～|~|——|一|－)(\w{3,4})($|。| )')

    try:
        destination = re.findall(destination_pattern,msg)[0][1]
    except :
        print("未找到Destination,取默认值")
        #晚上出发取廊坊，早上出发取北京
        if("早" in dayStr[0]):
            destination = "北京"
        else:
            destination = "廊坊"
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
    origin = origin
    destination = destination
    route = route
    seats = seats
    car_id = ''
    telephone = telephone
    message = msg
    description = getDescription(msg)

    # In[5]:

    sql = " INSERT INTO `aipin`.`aipin_route` ( `publisher`, `departure_time`, `departure_time_info`, `direction`, `origin`, `destination`, `route`, `seats`, `car_id`, `telephone`, `message`, `description`) VALUES ('%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" % (publisher, departure_time, departure_time_info, direction, origin, destination, route, seats, car_id,telephone,message,description)
    print(sql)

    return sql

    # In[2]:
#验证语句合法性
#必须包含时间信息：上午|下午|晚
# def formatChecker(s):
#     print("formatChecker")
#     index= 0
#     for sentence in s.sentences:
#         check_pattern = re.compile(r'上午|下午|晚|明早')
#         if (re.search(check_pattern, sentence)):
#             print("baseSentence: " + sentence)
#             return index
#         index = index + 1
#     return -1

def formatChecker(msg):
    print("formatChecker")
    index = 0
    check_pattern = re.compile(r'上午|下午|晚|明早')
    if (re.search(check_pattern, msg)):
        print("baseSentence: " + msg)
        return index
    return -1

#将字符串格式的时间 转化为时间格式
#dayStr : 今晚、晚上、明早
#timeStr : 7:10 等
#例：今晚7.10  =>  2018-09-20 19:10:00
def timeGenerator(dayStr,timeStr) :
    print("timeGenerator")
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
    print("getRoute")
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
    print("getDescription")
    description = ""
    description_pattern = re.compile(r'[\(（](.*?)[\)）]')
    resultArray = re.findall(description_pattern,msg)
    for i in resultArray:
        description = description + i + " "
    return description


#得到
def getOrigin(dayStr, route, msg, baseSentence):
    print("getOrigin")
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