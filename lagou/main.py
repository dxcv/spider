'''
主程序
'''

import pprint
import constant
from parse import parseInfo, parsePage
from getPage import GetPage
import os
import random


def work_start(baseurl, para):
    print('城市: %s' % para['city'])

    if para['kd'] == '':
        print('职位: 所有')
    else:
        print('职位: %s' % para['kd'])

    last_page = False

    my_requests = GetPage()

    while not last_page:
        print('开始读取第  %d  页' % para['pn'])

        info = my_requests.post(baseurl, para)
        last_page = parseInfo(info)

        para['pn'] += 1

    print('已经到达最后一页')


if __name__ == '__main__':

    para = {
        'first': 'true',
    }

    last_page = False

    siteurl = 'https://www.lagou.com/jobs/positionAjax.json'

    for city in constant.city_list:
        para['city'] = city
        if len(constant.kd_list) != 0:
            for kd in constant.kd_list:
                para['kd'] = kd
                para['pn'] = 1
                work_start(siteurl, para)
        else:
            para['kd'] = ''
            para['pn'] = 1
            work_start(siteurl, para)
