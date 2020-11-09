#/usr/bin/env python
# -*- coding: utf-8 -*-

import http.client   #原本是httplib
import hashlib
import json  #新增json库
import urllib
import random
import time
from bs4 import BeautifulSoup


def baidu_trans(content):
    appid = '20190508000295340' #你的appid
    secretKey = '6jCNCulCH1xpAkUEJZ9_' #你的密钥

    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = content   #要翻译的内容
    fromLang = 'zh'     #从什么语言
    toLang = 'en'       #翻译到什么语言
    salt = random.randint(32768, 65536)
    sign = appid+q+str(salt)+secretKey

    sign = hashlib.md5(sign.encode()).hexdigest()   #使用hashlib的函数替代之前的md5库的方法
    myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        #response是HTTPResponse对象
        response = httpClient.getresponse()
        jsonResponse = response.read().decode("utf-8")
        js = json.loads(jsonResponse)
        dst = str(js["trans_result"][0]["dst"])
        return dst
    except Exception as e:  #更改了except2.7到3.7的方法
        print ("err:"+ str(e))
    finally:
        if httpClient:
            httpClient.close()


print(baidu_trans("苹果"))