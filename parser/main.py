# -*- coding: utf-8 -*-

from lib.crawl_full_page import crawl
from lib.get_product_price import get_price
from lib.get_shop_rate import get_shop_rate
from lib.get_shop_qualification import get_qualification
from lib.get_shop_years import get_years
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
        res['price'] = price if price is not None else ''
        res['shop_rate'] = shop_rate if shop_rate is not None else ''
        res['qualification'] = qualification if qualification is not None else ''
        res['shop_years'] = shop_years if shop_years is not None else ''
        json_res = json.dumps(res)
    except Exception as e:
        print u'汇总信息异常，url =' + str(url)
        print e
        return json.dump({})

    return json_res

def main():
    url = "http://e22a.com/h.YLdb8E?cv=AAZeSonL&sm=398363"  #tmall
    url = "https://detail.tmall.com/item.htm?spm=a230r.1.14.159.ogQK1s&id=536443315513&ns=1&abbucket=8"
    # url = "https://item.taobao.com/item.htm?spm=a230r.1.14.237.ogQK1s&id=523362730050&ns=1&abbucket=8#detail"
    # html = crawl(url)
    # soup = BeautifulSoup(html)
    soup = BeautifulSoup(open("file/full_page/page.tmp.taobao"))
    soup.prettify()
    #资质
    qualification = get_qualification(soup)

    # fileName = 'file/full_page/page.tmp'
    # print u'写入临时文件'
    # write_to_txt(html, fileName, url)


    # js = commands.getstatusoutput('grep "<script>(function(w, d)" ' + fileName)
    # if len(js) < 20:
    #     js = commands.getstatusoutput('grep "sellerId" ' + fileName)
    # # commands.getstatusoutput('rm -f ' + fileName)
    #
    # # 获取销售id, 商品id
    # (sellerId, itemId) = get_itemId_sellerId(js)
    # # 获取评论并写入文件
    # get_comments(sellerId, itemId)


if __name__ == "__main__":
    main()
