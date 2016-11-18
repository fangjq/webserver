# -*- coding: utf-8 -*- #
# Author: Jiaquan Fang

import sys
from settings import settings
from parser.main import get_crawled_result

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
    url = "https://detail.tmall.com/item.htm?spm=a230r.1.14.159.ogQK1s&id=536443315513&ns=1&abbucket=://detail.tmall.com/item.htm?spm=a230r.1.14.159.ogQK1s&id=536443315513&ns=1&abbucket=8"
    print get_crawled_result(url)

