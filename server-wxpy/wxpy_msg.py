from wxpy import *
from CURD import *

# 打开数据库连接
db = pymysql.connect("localhost","lyn","lyn","aipin" )
list = []

#导入wxpy模块的全部内容
bot=Bot(cache_path=True, console_qr=True)
# 初始化机器人，电脑弹出二维码，用手机微信扫码登陆
bot.groups(update=True, contact_only=False)
#微信登陆后，更新微信群列表（包括未保存到通讯录的群）
my_groups=bot.groups().search('锦绣')
@bot.register(my_groups, except_self=False)
#注册消息响应事件，一旦收到铲屎群的消息，就执行下面的代码同步消息。机器人自己在群里发布的信息也进行同步。
def print_messages(msg):
    print(msg)
    if insertRoute(db,msg):
       pass
    else:
        list.append(msg)