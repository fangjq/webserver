# -*- coding: utf-8 -*-

from lib.crawl_full_page import crawl
from lib.get_product_price import get_price
from lib.get_shop_rate import get_shop_rate
from lib.get_shop_qualification import get_qualification
from lib.get_shop_years import get_years
from lib.get_product_comments import get_comments
from bs4 import BeautifulSoup
import json

import os
ROOT = os.path.dirname(os.path.abspath(__file__))
print ROOT
path = lambda *a: os.path.join(ROOT, *a)


def get_crawled_result(url):
    res = {}
    try:
        html = crawl(url)
        soup = BeautifulSoup(html)
        price = get_price(soup)
        shop_rate = get_shop_rate(soup)
        qualification = get_qualification(soup)
        shop_years = get_years(soup)
        comments = get_comments(html)

        res['price'] = price if price is not None else ''
        res['shop_rate'] = shop_rate if shop_rate is not None else ''
        res['qualification'] = qualification if qualification is not None else ''
        res['shop_years'] = shop_years if shop_years is not None else ''
        res['comments'] = comments if comments is not None else ''
        json_res = json.dumps(res)
    except Exception as e:
        print u'汇总信息异常，url =' + str(url)
        print e
        return json.dumps({})

    return json_res



