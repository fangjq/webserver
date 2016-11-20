# -*- coding: utf-8 -*-

import commands
import re
def get_transaction_rate(soup):
    div = soup.find('div', class_='tb-sell-counter')
    if div is None:
        return None
    trans_data = div.a['title']
    if trans_data is not None:
        group = re.search(u'.*天内已售出(\d+)件.*其中交易成功(\d+)件.*', trans_data)
        if group:
            total = float(group.group(1))
            success = float(group.group(2))
            if total == 0 :
                return 0
            rate = format(success/total, "0.2%")
            return rate
    return None






