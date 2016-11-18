# -*- coding: utf-8 -*-
import requests
from main import  get_crawled_result
from lib.geturls import get_urls
from parser.lib.crawl_full_page import crawl
from parser.lib.get_product_comments import get_comments
from parser.lib.writetofile import write_to_txt

def batch_test():
    urls = get_urls()
    for url in urls:
        json_res = get_crawled_result(url)
        # json_res = get_comments(url)
        print json_res



def single_test():

        url = "http://e22a.com/h.YLdb8E?cv=AAZeSonL&sm=398363"  # tmall
        url = "https://detail.tmall.com/item.htm?spm=a230r.1.14.159.ogQK1s&id=536443315513&ns=1&abbucket=8"
        url = "https://item.taobao.com/item.htm?spm=a230r.1.14.237.ogQK1s&id=523362730050&ns=1&abbucket=8#detail"
        url = "https://rate.taobao.com/user-rate-2a6429ee35dac9c8fc1ec33ed948f2a6.htm" #summary taobao shop
        html = crawl(url)
        print html
        # soup = BeautifulSoup(html)
        # soup = BeautifulSoup(open("file/full_page/page.tmp.taobao"))
        # soup.prettify()
        # 资质
        # qualification = get_qualification(soup)

        # fileName = 'file/page.tmp.summary.request'
        # print u'写入临时文件'
        # write_to_txt(html, fileName, url)

if __name__ == '__main__':
    # single_test()
    batch_test()