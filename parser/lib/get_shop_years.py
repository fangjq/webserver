# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup

def get_years(soup):
    parent_tag = soup.find('textarea', class_='ks-datalazyload')
    if parent_tag is None:
        return None
    new_soup = BeautifulSoup(parent_tag.string)
    if new_soup is None :
        return None
    finded = new_soup.find('span', class_='tm-shop-age-content')
    if not finded:
        return None
    group = re.search(u'.*(\d)年店', finded.text)
    if group :
        return str(group.group(1))
    return None
