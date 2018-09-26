from wxpy import *
from CURD import *
from wxpy.utils import start_new_thread

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
print(my_groups)
@bot.register(my_groups, except_self=False)
#注册消息响应事件，一旦收到铲屎群的消息，就执行下面的代码同步消息。机器人自己在群里发布的信息也进行同步。
def msgCollector(msg):    
    msgQueue.append(msg)
    print(msgQueue)

while len(msgQueue) > 0 :
    if insertRoute(db,msgQueue[0]):
        print("SUC")
        msgQueue = []
        pass
    else:
        print("FAIL")
        list.append(msgQueue)

#堵塞线程，让机器人保持运行 
embed()
