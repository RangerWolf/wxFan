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

    req_order_new = False
    req_oreder_new_words = [u"饭" , " fan", "+1"]

    req_cancel = False
    req_cancel_words = [u"取消", "-1"]

    # 先尝试从content之中抽取intent
    if content is None or content == u"@饭饭饭":
        return empty_data()

    if u"@饭饭饭" in content :
        content = content.replace(u"@饭饭饭", "")

    # 对content做预处理
    for word in req_oreder_new_words :
        if word in content:
            req_order_new = True
            tmp_content = content.replace(word, "")
            break

    for word in req_cancel_words :
        if word in content:
            req_cancel = True
            tmp_content = content.replace(word, "")
            break

    if req_cancel == False and req_order_new == False :
        tmp_content = content

    # 使用预处理的content与nickname 尝试获取psid
    psid = get_psid_smart(nickname, tmp_content)

    default_resp = u"您说的话我还不认识，\n\n" \
                   u"订饭支持的命令格式：  wenjun yang +1 或者 wenjun yang 或者 wenjun yang fan 或者 wenjun yang 饭 \n\n" \
                   u"取消订饭目前还不支持。"

    if psid is None :
        return u"目前还没有您的记录， 请输入您的英文名， 比如： wenjun yang"

    if req_order_new == True :
        return order_new(psid)

    if req_cancel == True :
        return order_cancel(nickname)

    return default_resp

def order_cancel(nickname) :
    # step 1: 获取order id
    # step 2: 根据order id 取消订单
    return u'目前还不支持取消'

def empty_data() :
    return u"出错：内容为空"

def order_new(psid_dict) :
    req_form = {}
    req_form['order'] = "e-1"
    req_form['psid'] = psid_dict['psid']
    req_form['depcode'] = psid_dict['depcode']
    resp = requests.post("http://10.206.131.12/api/order-new", data=req_form).text
    if resp.startswith("{") and resp.endswith("}"):
        data = json.loads(resp)

        ret_msg = ""
        if data['succeed_count'] > 0:
            ret_msg += '成功下了' + str(data['succeed_count']) + '份单.\n\n 目前因为正处于试运行阶段， 请自行登录cdcfan/确认';

        if data['rejected_count'] > 0:
            ret_msg += '有' + str(data['rejected_count']) + '份单因为过了饭点而无法预定.';

        if data['failure_count'] > 0:
            ret_msg += '有' + str(data['failure_count']) + '份单出错而无法预定. 请退出重新登录确认是否存在账号异常.';

        return ret_msg
    else:
        return "订饭失败：" + resp


def get_psid_smart(nickname, content) :
    """
    尝试从content  / nickname 获取psid
    先尝试从content获取psid ， 如果获取失败， 尝试从nickname 看看本地是否有缓存
    :param nickname:
    :param content:
    :return:
    """
    nickname = nickname.strip().lower()
    content = content.strip().lower()

    cache_file_name = os.path.join(cur_file_path, "psid_cache.json")

    # 先从本地缓存获取
    if os.path.exists(cache_file_name):
        fobj = open(cache_file_name, 'r')
        strdata = fobj.read()

        if strdata is not None and len(strdata.strip()) > 0:
            jsondata = json.loads(strdata)
            fobj.close()
            if content in jsondata:
                print "found nickname info in cache file， by content"

                if nickname not in jsondata :
                    jsondata[nickname] = jsondata[content]
                    with open(cache_file_name, 'w') as fp:
                        json.dump(jsondata, fp)

                return jsondata[content]

            if nickname in jsondata:
                print "found nickname info in cache file， by nickname"
                return jsondata[nickname]


    # 否则尝试从api获取并缓存到本地
    resp = requests.get("http://10.206.131.12/api/user-search?identity=%s" % content).text
    if resp != "404 Not Found":
        jsondata[content] = json.loads(resp)
        jsondata[nickname] = json.loads(resp)
        with open(cache_file_name, 'w') as fp:
            json.dump(jsondata, fp)

        return resp


if __name__ == '__main__':
    # print get_psid("wenjun yang")
    print smart_action("wenjun", "+1")