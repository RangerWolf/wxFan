# -*- coding:utf-8 -*-

import sys, os, json
import platform
import schedule
import thread
from datetime import datetime
import itchat, time
from itchat.content import *


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')



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
    print json.dumps(msg)
    if msg['isAt']:
        import requests
        try :
            ret_msg = requests.post("http://localhost:5678/smart_reply", data=json.dumps(msg)).text
            print "ret_msg:", ret_msg
            itchat.send("@" + msg['ActualNickName'] + " :" + ret_msg, msg['FromUserName'])
        except Exception, ex:
            print ex
            itchat.send("@" + msg['ActualNickName'] + " :" + u"服务器开小差啦~", msg['FromUserName'])
    else :
        if msg["Content"] in ["fan", "饭", "+1"] :
            itchat.send("@" + msg['ActualNickName'] + " :" + u'您是要订饭吗？ 订饭请直接@我 ^_^', msg['FromUserName'])

def auto_notify_fan(thread_name) :
    """
    每天3点钟， 自动提醒大家订饭
    :return:
    """
    def daily_notify() :
        print "now:", datetime.now()
        print "automatically message :", u"测试： 今天没订饭的同学们记得订饭哦"

        target_chatroom_nickname = "wxbot_dev"
        target_chatroom_nickname = u"CDC自动订饭群-Dev阶段"

        chatrooms = itchat.get_chatrooms()
        for room in chatrooms :
            if room['NickName'] == target_chatroom_nickname :
                room_id = room['UserName']
                print "send message to id:", room_id
                itchat.send(u"每天自动提醒： 今天没订饭的同学们记得订饭哦", room_id)

    schedule.every().day.at("15:15").do(daily_notify)

    while True:
        schedule.run_pending()
        time.sleep(10)

if __name__ == '__main__':
    enableCmdQR=True
    is_windows = any(platform.win32_ver())
    if is_windows :
        enableCmdQR = False

    itchat.auto_login(True, enableCmdQR=enableCmdQR)

    thread.start_new_thread(auto_notify_fan, ("test thread",))

    print json.dumps(itchat.get_chatrooms())

    itchat.run()
