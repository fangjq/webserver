# -*- coding:utf-8 -*-
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import xlrd
import xlwt
import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from xlutils.copy import copy
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


def new_excel(file=config.OUT_FILE):
    print u'发现写入目标不存在，正在创建文件', file
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    book.add_sheet('sheet1', cell_overwrite_ok=True)
    book.save(file)
    print u'已成功创建文件', file


def repeat_excel(word, file=config.OUT_FILE):
    print u'正在检测', word, u'是否存在于文件中'
    try:
        workbook = xlrd.open_workbook(file)
        sheet = workbook.sheet_by_index(0)
        words = sheet.col_values(0)
        if word in words:
            print u'用户名在excel中已经存在', word, u'跳过该用户'
            return True
        else:
            print u'用户名在excel中不存在，可以写入'
            return False
    except IOError, e:
        if 'No such file' in e.strerror:
            print u'匹配重复时未找到该文件', file
            new_excel(file)
            return False
        return False


def write_to_excel(contents, file=config.OUT_FILE):
    print u'正在写入到文本中', contents[0]
    try:
        rb = xlrd.open_workbook(file)
        sheet = rb.sheets()[0]
        row = sheet.nrows
        wb = copy(rb)
        sheet = wb.get_sheet(0)
        count = 0
        name = contents[0]
        if not repeat_excel(name, file):
            for content in contents:
                sheet.write(row, count, content)
                count = count + 1
                wb.save(file)
                print u'已成功写入到文件', file, u'第', row + 1, u'行'
        else:
            print u'旺旺已存在, 跳过写入文件', file

    except IOError:
        print u'未找到该文件', file
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        book.add_sheet('sheet1', cell_overwrite_ok=True)
        book.save(file)
        print u'已成功创建该文件', file
        write_to_excel(contents, file)


def write_info(infos, file=config.OUT_FILE):
    if len(infos) >= 4:
        name = infos[0]
        print u'准备将', name, u'写入文件'
        title = infos[1]
        url = infos[2]
        info = infos[3]
        if len(info) >= 3:
            date = info[1]
            comment = info[2]
            meta = info[3]
            contents = (name, date, comment, meta, title, url)
            write_to_excel(contents, file)
        else:
            print u'信息不全，跳过写入'
    else:
        print u'写入文件时发生错误，跳过写入'


def get_count():
    try:
        with open(config.COUNT_TXT, 'r') as f:
            page = f.read()
            if not page:
                return 0
            else:
                return page
    except Exception:
        print '不存在计数文件，可从开头开始抓取'
        return 0


def write_count(count, file):
    try:
        with open(file, 'w') as f:
            f.write(str(count))
            f.close()
    except TypeError:
        print u'页码写入失败'
