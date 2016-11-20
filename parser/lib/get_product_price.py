# -*- coding: utf-8 -*-

def filter_price(soup, tag, price_class):
    price_tag = soup.find_all(tag, class_=price_class)
    min_price = None
    for item in price_tag:
        curr_price = item.get_text()
        if '-' in curr_price:
            pos = curr_price.find('-')
            curr_price = curr_price[0:pos]
        try:
            curr_price = float(curr_price)
        except Exception as e:
            print u'价格转换出错 '
            print e
            return None
        if min_price is None:
            min_price = curr_price
        elif curr_price < min_price:
            min_price = curr_price
    return min_price



def get_price(soup):
    price = filter_price(soup, "span", "tm-price")
    if price is None:
        price = filter_price(soup, "em", "tb-rmb-num")
    return price


