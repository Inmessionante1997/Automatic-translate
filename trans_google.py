#########################2018-11-29更新###########################
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re
import requests
import json
import execjs
import http.client
import hashlib
import json
import urllib
import time
import random
#################百度翻译#######################baidu_translate(content, fromLang = 'ru', toLang = 'zh')
def baidu_translate(content, fromLang = 'ru', toLang = 'en'):
    appid = '20151113000005349'
    secretKey = 'osubCEzlGjzvw8qdQc41'
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = content
    # fromLang = 'ru'  # 源语言
    # toLang = 'zh'  # 翻译后的语言
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        jsonResponse = response.read().decode("utf-8")  # 获得返回的结果，结果为json格式
        js = json.loads(jsonResponse)  # 将json格式的结果转换字典结构
        dst = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果
        return dst
    except Exception as e:
        return e
    finally:
        if httpClient:
            httpClient.close()
            time.sleep(2)
###########################################

class Py4Js():

    def __init__(self):
        self.ctx = execjs.compile(""" 
		function TL(a) { 
		var k = ""; 
		var b = 406644; 
		var b1 = 3293161072; 

		var jd = "."; 
		var $b = "+-a^+6"; 
		var Zb = "+-3^+b+-f"; 

		for (var e = [], f = 0, g = 0; g < a.length; g++) { 
			var m = a.charCodeAt(g); 
			128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
			e[f++] = m >> 18 | 240, 
			e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
			e[f++] = m >> 6 & 63 | 128), 
			e[f++] = m & 63 | 128) 
		} 
		a = b; 
		for (f = 0; f < e.length; f++) a += e[f], 
		a = RL(a, $b); 
		a = RL(a, Zb); 
		a ^= b1 || 0; 
		0 > a && (a = (a & 2147483647) + 2147483648); 
		a %= 1E6; 
		return a.toString() + jd + (a ^ b) 
	}; 

	function RL(a, b) { 
		var t = "a"; 
		var Yb = "+"; 
		for (var c = 0; c < b.length - 2; c += 3) { 
			var d = b.charAt(c + 2), 
			d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
			d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
			a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
		} 
		return a 
	} 
	""")

    def getTk(self, text):
        return self.ctx.call("TL", text)


def google_trans(word, sl="zh-CN", tl="en"):
    # 中：zh-CN，英：en，俄:ru
    headers = {
        'cookie': '_ga=GA1.3.1163951248.1511946285; NID=131=XX0_dJsOrF47GXs2WNtO1MXyKVCK39bW4HXS0XZZ3ZYHTvMGOz8CVJe1G2XVwAJNF9MYOb1ngCqa_NegB6db2kgJ5A9hT3SScy0ag_L41wvtXHiPpNZweONFGHFNtWR_; 1P_JAR=2018-6-7-15',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }

    url = 'https://translate.google.cn/translate_a/single?client=t&sl=' + sl + '&tl=' + tl + '&hl='+ tl +'&dt=at&dt=bd&dt=ex&dt=ld&' \
                                                                                             'dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=0&tsel=0&kc=2&tk={tk}&q=' + word

    js = Py4Js()
    tk = js.getTk(word)
    url = url.format(tk=tk)
    # while
    try:
        s = requests.get(url, headers=headers)
        sj = s.json()
        trans = ''
        try:
            len(sj[1])
            trans += '[' + sj[1][0][0] + ']' + '\n'
            for i in sj[1][0][1]:
                trans += str(i) + ','
            trans = trans.rstrip(',')
        except:
            if len(sj[0]) > 1:
                for i in sj[0][:-1]:
                    trans += i[0] + '\n'
            elif len(sj[0]) == 1:
                trans = sj[0][0][0]+ '\n'
    except:
        trans = word
    trans = trans.replace("\n"," ")
    return trans

#SZn改写，效率较快
def google_szn_trans(word, sl="zh-CN", tl="en"):
    # 中：zh-CN，英：en，俄:ru
    headers = {
        'cookie': '_ga=GA1.3.1163951248.1511946285; NID=131=XX0_dJsOrF47GXs2WNtO1MXyKVCK39bW4HXS0XZZ3ZYHTvMGOz8CVJe1G2XVwAJNF9MYOb1ngCqa_NegB6db2kgJ5A9hT3SScy0ag_L41wvtXHiPpNZweONFGHFNtWR_; 1P_JAR=2018-6-7-15',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }

    url = 'https://translate.google.cn/translate_a/single?client=t&sl=' + sl + '&tl=' + tl + '&hl='+ tl +'&dt=at&dt=bd&dt=ex&dt=ld&' \
                                                                                             'dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=0&tsel=0&kc=2&tk={tk}&q=' + word

    js = Py4Js()
    tk = js.getTk(word)
    url = url.format(tk=tk)
    # while
    result = {"pos": "", "mean": []}
    try:
        s = requests.get(url, headers=headers)
        sj_lst = s.json()
        if sj_lst[0][0][0] != None:
            result["mean"].append((sj_lst[0][0][0], 1.0))
        if sj_lst[1] != None:
            result["pos"] = sj_lst[1][0][0]
            for item in sj_lst[1][0][2]:
                if item[-1] > 0.001:
                    result["mean"].append((item[0], item[-1]))
                else:
                    break
    except:
        pass
    return result

#SZn改写，翻译句子
def google_szn_trans_sentence(sentence, sl="zh-CN", tl="en"):
    # 中：zh-CN，英：en，俄:ru
    headers = {
        'cookie': '_ga=GA1.3.1163951248.1511946285; NID=131=XX0_dJsOrF47GXs2WNtO1MXyKVCK39bW4HXS0XZZ3ZYHTvMGOz8CVJe1G2XVwAJNF9MYOb1ngCqa_NegB6db2kgJ5A9hT3SScy0ag_L41wvtXHiPpNZweONFGHFNtWR_; 1P_JAR=2018-6-7-15',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }

    url = 'https://translate.google.cn/translate_a/single?client=t&sl=' + sl + '&tl=' + tl + '&hl='+ tl \
          +'&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=0&tsel=0&kc=2&tk={tk}&q=' + sentence

    js = Py4Js()
    tk = js.getTk(sentence)
    url = url.format(tk=tk)
    # while
    result = ""
    try:
        s = requests.get(url, headers=headers)
        sj_lst = s.json()
        if len(sj_lst[0])==1:
            result = sj_lst[0][0][0]
        else:
            for x in sj_lst[0][:-1]:
                result += x[0]
    except:
        pass
    return result

# 利用第三方端口：http://www.liuyanlin.cn/get_translate翻译
def google_liu_trans(word, sl="zh-CN", tl="en"):
    headers = {
        'cookie': '_ga=GA1.3.1163951248.1511946285; NID=131=XX0_dJsOrF47GXs2WNtO1MXyKVCK39bW4HXS0XZZ3ZYHTvMGOz8CVJe1G2XVwAJNF9MYOb1ngCqa_NegB6db2kgJ5A9hT3SScy0ag_L41wvtXHiPpNZweONFGHFNtWR_; 1P_JAR=2018-6-7-15',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }
    url = "http://www.liuyanlin.cn/get_translate?sl="+sl+"&tl="+tl+"&wd="+word
    s = requests.get(url, headers=headers)
    sj_lst = s.json()["data"]
    result = {"pos":"","mean":[]}
    try:
        if sj_lst[0][0][0] != None:
            result["mean"].append((sj_lst[0][0][0], 1.0))
        if sj_lst[1] != None:
            result["pos"] = sj_lst[1][0][0]
            for item in sj_lst[1][0][2]:
                if item[-1] > 0.001:
                    result["mean"].append((item[0], item[-1]))
                else:
                    break
    except:
        pass
    return result

#实用爬虫，从俄文网站翻译，尚未完成此功能
def ru_trans(word):
    headers = {
        'cookie': '_ga=GA1.3.1163951248.1511946285; NID=131=XX0_dJsOrF47GXs2WNtO1MXyKVCK39bW4HXS0XZZ3ZYHTvMGOz8CVJe1G2XVwAJNF9MYOb1ngCqa_NegB6db2kgJ5A9hT3SScy0ag_L41wvtXHiPpNZweONFGHFNtWR_; 1P_JAR=2018-6-7-15',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }
    url = "https://bkrs.info/slovo.php?ch=" + word
    result = None
    try:
        s = requests.get(url, headers=headers)
        result = s.text
    except:
        pass
    return result

from urllib import parse
#SZn改写，获取完整的翻译列表信息
def google_szn_trans_lst(word, sl="zh-CN", tl="en"):
    # 中：zh-CN，英：en，俄:ru
    headers = {
        'cookie': '_ga=GA1.3.1163951248.1511946285; NID=131=XX0_dJsOrF47GXs2WNtO1MXyKVCK39bW4HXS0XZZ3ZYHTvMGOz8CVJe1G2XVwAJNF9MYOb1ngCqa_NegB6db2kgJ5A9hT3SScy0ag_L41wvtXHiPpNZweONFGHFNtWR_; 1P_JAR=2018-6-7-15',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }
    # word = {'q': word}
    # word = parse.urlencode(word)
    # word = word.replace("+","%20")
    url = 'https://translate.google.cn/translate_a/single?client=t&sl=' + sl + '&tl=' + tl + '&hl='+ tl +'&dt=at&dt=bd&dt=ex&dt=ld&' \
                                                                                             'dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=0&tsel=0&kc=2&tk={tk}&q=' + word

    js = Py4Js()
    tk = js.getTk(word)
    url = url.format(tk=tk)
    # while
    result = None
    try:
        s = requests.get(url, headers=headers)
        result = s.json()
    except:
        pass
    return result

#http://www.liuyanlin.cn/get_translate?sl=zh-CN&tl=en&wd=北京

import pickle as pkl
if __name__ == '__main__':
    # x = google_trans("идиоты",tl="en")#,tl="en"
    x = google_szn_trans_sentence("这本书很烂",tl="en")#,tl="en"
    print(x)
    # x = google_szn_trans("идиоты", sl="ru", tl="zh-CN")
    # print(x)
    # y = google_szn_trans("идиоты", sl="ru", tl="en")
    # print(y)

    # s = "Один из самых молодых проектов МГЕР Санкт Петербурга продолжает активно развиваться"
    # z = google_szn_trans(s, sl="ru", tl="en")
    # print(z)
    # import pickle as pkl
    # from senticnet.senticnet import SenticNet
    # sn_en = SenticNet()
    # sn_ru = SenticNet("ru")
    #
    # id2word = pkl.load(open('process_data_fb/id2word_en_senti', 'rb'))
    # for item in id2word.items():
    #     if isinstance(id2word[item[0]],tuple) and len(id2word[item[0]])==3:
    #         print(item[0], id2word[item[0]])
    #         continue
    #     if item[0]<=14:
    #         id2word[item[0]] = (item[1],item[1],0)
    #     else:
    #         en_trans = None
    #         try:
    #             en_trans = google_szn_trans(item[1], sl="ru", tl="en")["mean"][0][0]
    #             score = float(sn_ru.polarity_value(item[1]))
    #         except:
    #             try:
    #                 score = float(sn_en.polarity_value(en_trans))
    #             except:
    #                 score = 0
    #         id2word[item[0]] = (item[1], en_trans, score)
    #     print(item[0], id2word[item[0]])
    #     if item[0]%100==0:
    #         pkl.dump(id2word, open('process_data_fb/id2word_en_senti2', 'wb'))
    #
    s = "ахуенными"
    ru_trans(s)
    # z = google_szn_trans(s, sl="ru", tl="en")
    # print(z)
    # re_data_list, word_set = pkl.load(open('process_data_fb/r&e_data_list2', 'rb'))
    # word_lst = list(word_set)
    # word_lst.sort()
    # for i,wrd in enumerate(word_lst):
    #     print(i,wrd)
