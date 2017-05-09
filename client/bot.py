# -*- coding:utf-8 -*-

import sys, os, json
import platform
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')


import itchat, time
from itchat.content import *

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg['isAt']:
        import requests
        ret_msg = requests.post("http://localhost:5678/smart_reply", data=json.dumps(msg)).text
        print "ret_msg:", ret_msg
        itchat.send("@" + msg['ActualNickName'] + " :" + ret_msg, msg['FromUserName'])
    else :
        if msg["Content"] in ["fan", "饭", "+1"] :
            itchat.send("@" + msg['ActualNickName'] + " :" + u'您是要订饭吗？ 订饭请直接@我 ^_^', msg['FromUserName'])

enableCmdQR=True
is_windows = any(platform.win32_ver())
if is_windows :
    enableCmdQR = False

itchat.auto_login(True, enableCmdQR=enableCmdQR)
itchat.run()
