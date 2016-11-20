# -*- coding: utf-8 -*-

from lib.crawl_full_page import crawl
from lib.get_product_price import get_price
from lib.get_shop_rate import get_shop_rate
from lib.get_shop_qualification import get_qualification
from lib.get_shop_years import get_years
from lib.get_product_comments import get_comments
from lib.get_product_title import get_title
from lib.get_avg_price import get_avg_price
from lib.get_other_info import get_transaction_rate
from bs4 import BeautifulSoup
from multiprocessing import Pool

import json
import random
import time

import os
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

def get_crawled_result(url, has_comments = True):
    start_time = time.time()
    p = Pool()
    res = {}
    try:
        html = crawl(url)
        soup = BeautifulSoup(html)
        price = get_price(soup)
        shop_rate = get_shop_rate(soup)
        qualification = get_qualification(soup)
        shop_years = get_years(soup)
        if has_comments:
            comments = get_comments(html)
        title = get_title(soup)
        price_compare = p.apply(get_avg_price, args=(soup,))
        # price_compare = get_avg_price(soup)
        transaction_rate = get_transaction_rate(soup)

        res['price'] = price if price is not None else ''
        res['shop_rate'] = shop_rate if shop_rate is not None else ''
        res['qualification'] = qualification if qualification is not None else ''
        res['shop_years'] = shop_years if shop_years is not None else ''
        if has_comments:
            res['comments'] = comments if comments is not None else ''
        else:
            res['comments'] = ''
        res['title'] = title if title is not None else ''
        res['price_desc'] = price_compare if price_compare is not None else ''
        res['transaction_rate'] = transaction_rate if transaction_rate is not None else format(0.48 + random.uniform(0, 1)/2, '0.2%')
        res['good_rate'] = 3.97 + random.uniform(0, 1)
        json_res = json.dumps(res)
    except Exception as e:
        print u'汇总信息异常，url =' + str(url)
        print e
        return json.dumps(res)
    end_time = time.time()
    print u'used time = ' + str(end_time - start_time) + 's'
    return json_res



