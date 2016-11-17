# -*- coding: utf-8 -*-
import random
import re

import requests
import json

import time


def get_itemId_sellerId(html):
    sellerId = None
    itemId = None
    matchObj = re.match(r'.*sellerId=(\d+)&amp;itemId=(\d+).*', html, re.M | re.I)
    if matchObj:
        sellerId = matchObj.group(1)
        itemId = matchObj.group(2)
        print "sellerId : ", matchObj.group(1)
        print "itemId: ", matchObj.group(2)
    else:
        print "No match!!"

    return (sellerId, itemId)

def get_detail_comments(url):
    r = requests.get(url)
    complete_json = '{' + r.text + "}"
    print complete_json
    try:
        map = json.loads(complete_json)
    except Exception :
        print u'抓取评论内容出错，被屏蔽'
        time.sleep(random.uniform(1, 5))
        try:
            map = json.loads(complete_json)
        except Exception:
            map = dict()
    return map


def get_comments(sellerId, itemId):
    if sellerId is None or itemId is None:
        return None
    url_head = "http://rate.tmall.com/list_detail_rate.htm?itemId=" + str(itemId) + "&sellerId=" + str(sellerId)
    all_content = get_detail_comments(url_head)
    lastPage = all_content["rateDetail"]["paginator"]["lastPage"]

    for currentPage in range(1, lastPage):
        print 'page = ' + str(currentPage)
        url = url_head + "&currentPage=" + str(currentPage)
        all_content = get_detail_comments(url)
        if("rateDetail" not in all_content):
            print u'抓取发生异常，跳过'
            continue
        rateList = all_content["rateDetail"]["rateList"]
        for rate in rateList:
            print "rateContent = " + rate["rateDate"] + "\t" + rate["rateContent"]



if __name__ == "__main__":
    html = '<!DOCTYPE html><html class="w990 ks-webkit538 ks-webkit ks-safari2 ks-safari"><head><script charset="gbk" src="https://bar.tmall.com/cueAssetMsg.htm?sellerId=890482188&amp;itemId=540219887479&amp;brandId=&amp;frontEndCatId=&amp;bizId=&amp;bizInfo=..pc&amp;_ksTS=1479348797763_2535&amp;callback=__mallbarCueAssetMsg&amp;_input_charset=UTF-8" async=""></script><script charset="gbk" src="https://fragment.tmall.com/tmbase/mallbar_3_2_16?bizInfo=..pc&amp;_ksTS=1479348797540_2388&amp;callback=__mallbarGetConf&amp;_input_charset=UTF-8" async=""></script><script charset="gbk" src="https://bar.tmall.com/getMallBar.htm?sellerNickName=nike%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97&amp;bizInfo=..pc&amp;_ksTS=1479348797133_2375&amp;callback=__mallbarGetMallBar&amp;shopId=71955116&amp;v=3.2.4&amp;bizId=&amp;sellerId=890482188&amp;itemId=540219887479&amp;_input_charset=UTF-8" async=""></script><script charset="utf8" src="https://g.alicdn.com/sd/data_sufei/1.3.6/sufei/??sufei-min.js?t=1_2013072520131122.js" async=""></script><script src="https://amos.alicdn.com/muliuserstatus.aw?_ksTS=1479348791485_2340&amp;callback=jsonp2341&amp;beginnum=0&amp;charset=utf-8&amp;uids=nike%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97&amp;site=cntaobao" async=""></script><script src="https://g.alicdn.com/aliww/web.ww.im/0.1.9/scripts/adapter.js"></script><script charset="utf-8" src="https://g.alicdn.com/??mui/mallbar/3.2.22/index.js,kissy/k/1.4.2/swf-min.js,kissy/k/1.4.2/xtemplate-min.js,kissy/k/1.4.2/xtemplate/compiler-min.js,mui/mallbar/3.2.22/conf.js,mui/mallbar/3.2.22/util.js,mui/mallbar/3.2.22/model.js,mui/mallbar/3.2.22/store.js,mui/storage/3.0.5/index.js,mui/storage/3.0.5/conf.js,mui/storage/3.0.5/util.js,mui/storage/3.0.5/xd.js,mui/storage/3.0.5/name.js,mui/mallbar/3.2.22/mallbar-item.js,mui/ma'
    (sellerId, itemId) = get_itemId_sellerId(html)
    get_comments(sellerId, itemId)
