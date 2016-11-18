# -*- coding: utf-8 -*-

def get_title(soup):
    title = soup.title
    if title is not None :
        title = title.string
        if '|' in title:
            pos = title.find('|')
            title = title[0:pos]
        title = title.rstrip(u'-tmall.com天猫')
        title = title.rstrip(u'-淘宝网')
    return title