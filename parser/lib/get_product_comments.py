# -*- coding: utf-8 -*-
import random
import re

import requests
import json

import time
import sys
sys.path.append('../')
import config
import commands
from crawl_full_page import crawl
from writetofile import write_to_txt

COMMENTS_FILE = 'file/comments.list'

def get_itemId_sellerId(html):
    print u'正则匹配itemId和sellerId'
    sellerId = None
    itemId = None
    #g_config={itemId:"520962184315",sellerId:"260030441",
    # pattern = r'.*sellerId=(\d+)&amp;itemId=(\d+).*'
    pattern = r'.*itemId:"(\d+).{1,30}sellerId:"(\d+)"'
    matchObj = re.search(pattern, str(html), re.M | re.I)
    if matchObj:
        itemId = matchObj.group(1)
        sellerId = matchObj.group(2)
    else:
        #itemId=523362730050&sellerId=126732883
        matchObj = re.search(r'.*itemId=(\d+)&sellerId=(\d+)', str(html), re.M | re.I)
        if matchObj:
            itemId = matchObj.group(1)
            sellerId = matchObj.group(2)
        else:
            print "No match!!"

    return (sellerId, itemId)

def get_detail_comments(url):
    crawled_json = crawl(url, False)
    complete_json = '{' + crawled_json + '}'
    try:
        map = json.loads(complete_json, encoding='utf-8')
    except Exception:
        print u'被封了，休息一会'
        time.sleep(random.randint(0, 1))
        return {}
    return map


def get_comments_by_sellerId_itemId(sellerId, itemId, is_write_to_file=True):
    ret = []
    if sellerId is None or itemId is None:
        return None
    url_head = "http://rate.tmall.com/list_detail_rate.htm?itemId=" + str(itemId) + "&sellerId=" + str(sellerId)
    all_content = get_detail_comments(url_head)
    if all_content.has_key("rateDetail"):
        lastPage = all_content["rateDetail"]["paginator"]["lastPage"]
        lastPage = lastPage if lastPage < config.MAX_PAGE_SIZE else config.MAX_PAGE_SIZE
    else:
        lastPage = 2
    for currentPage in range(1, lastPage):
        print u'抓取评论第' + str(currentPage) + u'页'
        url = url_head + "&currentPage=" + str(currentPage)
        all_content = get_detail_comments(url)
        if("rateDetail" not in all_content):
            print u'抓取发生异常，跳过'
            continue
        rateList = all_content["rateDetail"]["rateList"]
        for rate in rateList:
            comments = rate["rateDate"] + '\t' + rate["rateContent"] + '\t' + url
            if is_write_to_file:
                write_to_txt(comments, COMMENTS_FILE, rate["rateContent"] + url)
            map = {}
            map['comment_date'] = rate["rateDate"]
            map['comment_content'] = rate['rateContent']
            ret.append(map)
    return ret



def get_comments(html):
    fileName = 'file/full_page/page.tmp'
    write_to_txt(html, fileName)
    js = commands.getstatusoutput('grep "<script>(function(w, d)" ' + fileName)
    if js is None or len(js) < 20:
        js = commands.getstatusoutput('grep "sellerId" ' + fileName)
    commands.getstatusoutput('rm -f ' + fileName)

    # 获取销售id, 商品id
    (sellerId, itemId) = get_itemId_sellerId(js)
    # 获取评论并写入文件
    return get_comments_by_sellerId_itemId(sellerId, itemId, False)


