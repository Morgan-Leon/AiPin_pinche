from wxpy import *

#导入wxpy模块的全部内容
bot=Bot(cache_path=True, console_qr=True)
# 初始化机器人，电脑弹出二维码，用手机微信扫码登陆
bot.groups(update=True, contact_only=False)
#微信登陆后，更新微信群列表（包括未保存到通讯录的群）
my_groups=bot.groups().search('16-501')
print(my_groups)