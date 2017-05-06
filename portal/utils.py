# -*- coding:utf-8 -*-

import sys, os, json
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')
cur_file_path = os.path.dirname(os.path.realpath(__file__))

def smart_action(nickname, content) :
    """
    根据content进行意图猜测
    :param content: 
    :return: 
    """
    if content is None or content == u"@饭饭饭":
        return empty_data()

    if u"@饭饭饭" in content :
        content = content.replace(u"@饭饭饭", "")

    if "-1" in content :
        tmp_content = content.replace("-1", "")
        return order_cancel()

    # 有可能内容就是英文名
    if "+1" in content :
        tmp_content = content.replace("+1", "")
    else :
        tmp_content = content
    resp = get_psid(tmp_content)
    if resp is not None :
        return order_new(tmp_content)

    if content == "fan" or u"饭" in content or content == "+1":
        return order_new(nickname)

    if content == "cancel" or u"取消" in content :
        return order_cancel(nickname)

    return u"你说的话我还不认识：" + content

def order_cancel(nickname) :
    # step 1: 获取order id
    # step 2: 根据order id 取消订单
    return u'目前还不支持取消'

def empty_data() :
    return u"出错：内容为空"

def order_new(nickname) :
    # step1 : 根据nickname获取其工号与部门代码
    resp = get_psid(nickname)
    if resp is None :
        return u"还不知道你的工号, 请告诉我你的英文名, 比如: wenjun yang"

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


def get_psid(nickname) :
    cache_file_name = os.path.join(cur_file_path, "psid_cache.json")
    jsondata = {}
    # 先从本地缓存获取
    if os.path.exists(cache_file_name) :
        fobj = open(cache_file_name, 'r')
        strdata = fobj.read()

        if strdata is not None and len(strdata.strip()) > 0 :
            jsondata = json.loads(strdata)
            fobj.close()
            if nickname in jsondata :
                print "found nickname info in cache file"
                return jsondata[nickname]

    # 否则尝试从api获取并在本地缓存
    resp = requests.get("http://10.206.131.12/api/user-search?identity=%s" % nickname).text
    if resp == "404 Not Found":
        return None
    else :
        jsondata[nickname] = json.loads(resp)
        with open(cache_file_name, 'w') as fp:
            json.dump(jsondata, fp)

        return resp



if __name__ == '__main__':
    get_psid("wenjun yang")