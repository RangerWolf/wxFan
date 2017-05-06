# -*- coding:utf-8 -*-

import sys, os, json
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')


def smart_action(nickname, content) :
    """
    根据content进行意图猜测
    :param content: 
    :return: 
    """
    if content is None :
        return empty_data()

    if content == "fan" or u"饭" in content:
        return order_new(nickname)

    if content == "cancel" or u"取消" in content :
        return order_cancel(nickname)

def order_cancel(nickname) :
    # step 1: 获取order id
    # step 2: 根据order id 取消订单
    pass

def empty_data() :
    return "出错：内容为空"

def order_new(nickname) :
    # step1 : 根据nickname获取其工号与部门代码
    resp = requests.get("http://10.206.131.12/api/user-search?identity=%s" % nickname).text
    if resp == "404 Not Found":
        return u"自动寻找工号失败， 请将你的昵称改成类似：wenjun yang的形式"

    psid = json.loads(resp)['psid']
    depcode = json.loads(resp)['depcode']

    # step2 : 调用订饭api
    req_form = {}
    req_form['order'] = "e-1"
    req_form['psid'] = psid
    req_form['depcode'] = depcode
    resp = requests.post("http://10.206.131.12/api/order-new", data=req_form).text
    if resp.startswith("{") and resp.endswith("}"):
        data = json.loads(resp)

        ret_msg = ""
        if data['succeed_count'] > 0:
            ret_msg += '成功下了' + str(data['succeed_count']) + '份单.\n';

        if data['rejected_count'] > 0:
            ret_msg += '有' + str(data['rejected_count']) + '份单因为过了饭点而无法预定.\n';

        if data['failure_count'] > 0:
            ret_msg += '有' + str(data['failure_count']) + '份单出错而无法预定. 请退出重新登录确认是否存在账号异常.\n';

        return ret_msg
    else:
        return "订饭失败：" + resp