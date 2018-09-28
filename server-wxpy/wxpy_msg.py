from wxpy import *
import pymysql
from allInOne import *

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
        for group in my_groups:
            if group == msg.chat:
                continue
            insertRoute(db,msg)

    process()

# def sync_my_groups(msg):
#     sync_message_in_groups(msg, my_groups,run_async=False)
    #同步“铲屎官1群”和“铲屎官2群”的消息。包括文字、图片、视频、语音、文件、分享、普通表情、地图等。


#堵塞线程，让机器人保持运行 
bot.join()
