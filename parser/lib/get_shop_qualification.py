# -*- coding: utf-8 -*-

def get_qualification(soup):
    ret = {}
    parent_tag = soup.find('div', class_="tb-shop-icon")
    if parent_tag is None:
        return None
    finded = parent_tag.find("dt", text=u'资质：')
    if not finded:
        return None
    qualification = finded.parent.find('dd').text.strip()
    print qualification
    ret['qualification'] = qualification
    return ret
