# -*- coding: utf-8 -*-
import random
import re

import requests
import json

import time
import sys
from bs4 import BeautifulSoup
from crawl_full_page import crawl



def filter_shop_rate_taobao(soup, tag, class_name):
    ret = {}
    parentTag = soup.find(tag, class_=class_name)
    if parentTag is None:
        return None
    has_desc = parentTag.find("dt", text=u'描述')
    if not has_desc:
        return None
    desc = parentTag.find("dt", text=u'描述').parent.find('dd').text.strip()
    service = parentTag.find("dt", text=u'服务').parent.find('dd').text.strip()
    logistics = parentTag.find("dt", text=u'物流').parent.find('dd').text.strip()
    ret['desc'] = desc
    ret['service'] = service
    ret['logistics'] = logistics
    return ret

def filter_shop_rate_tmall(soup, tag, class_name):
    ret = {}
    parentTag = soup.find(tag, class_=class_name)
    if not parentTag:
        return None
    textarea = parentTag.find('textarea', class_="ks-datalazyload")
    if not textarea:
        return None
    soup = BeautifulSoup(textarea.string)
    lis = soup.findAll('li')
    for li in lis:
        li_val = li.text.strip()
        pattern = r'.*(\d.\d)'
        group = re.search(pattern, li_val)
        if group:
            count = group.group(1)
            if li_val.startswith(u'描述') :
                ret["desc"] = count
            elif li_val.startswith(u'服务') :
                ret["service"] = count
            elif li_val.startswith(u'发货') :
                ret["logistics"] = count
    if len(ret) != 3:
        print u'获取店铺评分失败'
        return None
    return ret


def get_shop_rate(soup):
    rates = filter_shop_rate_taobao(soup, "div", "tb-shop-info-bd")
    if rates is None:
        rates = filter_shop_rate_tmall(soup, "div", "extra-info")
    return rates


