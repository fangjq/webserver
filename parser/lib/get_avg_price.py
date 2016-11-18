# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from get_product_price import get_price
from get_links import get_results
from get_product_title import get_title


def get_avg_price(soup):
    price = get_price(soup)
    if price is None:
        print None
    title = get_title(soup)
    if title is None:
        return None
    print title
    html = get_results(title, False)
    soup = BeautifulSoup(html)
    if soup is None :
        return None
    pr_list = []
    for pr in soup.find_all('p', class_="productPrice"):
        try:
            val = float(pr.text.strip().strip(u'¥'))
            pr_list.append(val)
        except Exception as e:
            print u'数字转换异常'
            print e
            continue
    if len(pr_list) == 0 :
        return None

    total = 0.0
    top = 20
    print pr_list
    for item in pr_list[0:top]:
        if abs((price - item) / item) > 0.5:
            continue
        total += item
    avg = total / top
    rate = format(abs((price - avg) / avg), '0.1%')
    if price < avg:
        return u'比同类产品低' + str(rate)
    else:
        return u'比同类产品高' + str(rate)


