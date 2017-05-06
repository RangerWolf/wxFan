# -*- coding:utf-8 -*-

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask
from flask import request, url_for, redirect
import json
import utils
app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def hello_world():
    return 'Hello World!'

@app.route('/smart_reply', methods=["POST", "GET"])
def smart_reply():
    data = request.data     # 从客户端发送上来的数据
    if data is None or len(data.strip()) == 0 :
        return "Empty Data"

    msg = json.loads(data) # 将其转成json obj的方式
    sender_nickname = msg['ActualNickName']
    sender_content  = msg['Content']

    ret_msg = utils.smart_action(sender_nickname, sender_content)

    return ret_msg

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)