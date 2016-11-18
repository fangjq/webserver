# -*- coding: utf-8 -*-

from lib.get_product_comments import get_comments_by_sellerId_itemId
from lib.get_product_comments import get_itemId_sellerId
import config

from lib.writetofile import write_count, get_count
from lib.geturls import get_urls
from lib.crawl_full_page import crawl
from lib.writetofile import write_to_txt
import commands

def main():
    urls = get_urls()
    print u'获取到如下链接列表'
    # print urls
    config.TOTAL_COUNT = len(urls)
    print u'共有', config.TOTAL_COUNT, u'个链接'
    count = int(get_count())
    if count < config.TOTAL_COUNT:
        for count in range(count, config.TOTAL_COUNT):
            try:
                write_count(count, config.COUNT_TXT)
                url = urls[count]
                print u'正在爬取第', count + 1, u'个网页, 共', config.TOTAL_COUNT, u'个'
                config.NOW_COUNT = count
                html = crawl(url)
                fileName = 'file/full_page/page.' + str(count)
                print u'写入临时文件'
                write_to_txt(html, fileName, url)
                print u'当前已完成采集', config.NOW_COUNT + 1, u'个, 共', config.TOTAL_COUNT, u'个'
                js = commands.getstatusoutput('grep "<script>(function(w, d)" ' + fileName)
                if len(js) < 20:
                    js = commands.getstatusoutput('grep "sellerId" ' + fileName)
                # commands.getstatusoutput('rm -f ' + fileName)

                count = count + 1
                # 获取销售id, 商品id
                (sellerId, itemId) = get_itemId_sellerId(js)
                # 获取评论并写入文件
                get_comments_by_sellerId_itemId(sellerId, itemId)
            except Exception as e:
                count = count + 1
                print u'程序异常，跳过url: ' + url
                print e


        print u'采集结束,完成了', len(urls), u'个链接的采集'
    else:
        print u'链接上次已经全部爬取完毕'


# def test():
#     html = '<!DOCTYPE html><html class="w990 ks-webkit538 ks-webkit ks-safari2 ks-safari"><head><script charset="gbk" src="https://bar.tmall.com/cueAssetMsg.htm?sellerId=890482188&amp;itemId=540219887479&amp;brandId=&amp;frontEndCatId=&amp;bizId=&amp;bizInfo=..pc&amp;_ksTS=1479348797763_2535&amp;callback=__mallbarCueAssetMsg&amp;_input_charset=UTF-8" async=""></script><script charset="gbk" src="https://fragment.tmall.com/tmbase/mallbar_3_2_16?bizInfo=..pc&amp;_ksTS=1479348797540_2388&amp;callback=__mallbarGetConf&amp;_input_charset=UTF-8" async=""></script><script charset="gbk" src="https://bar.tmall.com/getMallBar.htm?sellerNickName=nike%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97&amp;bizInfo=..pc&amp;_ksTS=1479348797133_2375&amp;callback=__mallbarGetMallBar&amp;shopId=71955116&amp;v=3.2.4&amp;bizId=&amp;sellerId=890482188&amp;itemId=540219887479&amp;_input_charset=UTF-8" async=""></script><script charset="utf8" src="https://g.alicdn.com/sd/data_sufei/1.3.6/sufei/??sufei-min.js?t=1_2013072520131122.js" async=""></script><script src="https://amos.alicdn.com/muliuserstatus.aw?_ksTS=1479348791485_2340&amp;callback=jsonp2341&amp;beginnum=0&amp;charset=utf-8&amp;uids=nike%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97&amp;site=cntaobao" async=""></script><script src="https://g.alicdn.com/aliww/web.ww.im/0.1.9/scripts/adapter.js"></script><script charset="utf-8" src="https://g.alicdn.com/??mui/mallbar/3.2.22/index.js,kissy/k/1.4.2/swf-min.js,kissy/k/1.4.2/xtemplate-min.js,kissy/k/1.4.2/xtemplate/compiler-min.js,mui/mallbar/3.2.22/conf.js,mui/mallbar/3.2.22/util.js,mui/mallbar/3.2.22/model.js,mui/mallbar/3.2.22/store.js,mui/storage/3.0.5/index.js,mui/storage/3.0.5/conf.js,mui/storage/3.0.5/util.js,mui/storage/3.0.5/xd.js,mui/storage/3.0.5/name.js,mui/mallbar/3.2.22/mallbar-item.js,mui/ma'
#     (sellerId, itemId) = get_itemId_sellerId(html)
#     get_comments(sellerId, itemId)


