import os

requests_header = {
    'Host':
    u'www.lagou.com',
    'User-Agent':
    u'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:u54.0) Gecko/20100101 Firefox/54.0',
    'Accept':
    u'application/json, text/javascript, */*; q=0.01',
    'Accept-Language':
    u'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding':
    u'gzip, deflate, br',
    'Referer':
    u'https:u//www.lagou.com/jobs/list_%E8%A5%BF%E5%AE%89?labelWords=&fromSearch=true&suginput=',
    'Content-Type':
    u'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With':
    u'XMLHttpRequest',
    'X-Anit-Forge-Token':
    u'None',
    'X-Anit-Forge-Code':
    u'0',
    'Content-Length':
    u'19',
    'Cookie':
    u'JSESSIONID=ABAAABAAAIAACBI54403B875C4101733BE49B9167420FC5; user_trace_token=20170725095533-0e2515f491f0475a834b8082dc9e6d72; _ga=GA1.2.492542911.1500947733; _gid=GA1.2.359578653.1500947733; LGRID=20170725150614-bf6d8cff-7107-11e7-b67d-5254005c3644; LGUID=20170725095533-589e2a8d-70dc-11e7-b534-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1500948816,1500948887,1500964278,1500964281; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1500966374; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_search; SEARCH_ID=6988992079e148718256b0cd49941534; X_HTTP_TOKEN=c8b09df4706ba5e70a426e3bbd13cb1f; _putrc=""; login=false; unick=""; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; LGSID=20170725143118-de2c5446-7102-11e7-b82d-525400f775ce',
    'Connection':
    u'keep-alive'
}

User_Agent = [{
    'User-Agent':
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0)'
    'Gecko/20100101 Firefox/34.0'
}, {
    'User-Agent':
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6)'
    'Gecko/20091201 Firefox/3.5.6'
}, {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11'
    '(KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'
}, {
    'User-Agent':
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'
}, {
    'User-Agent':
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0)'
    'Gecko/20100101 Firefox/40.0'
}, {
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64)'
    'AppleWebKit/537.36 (KHTML, like Gecko)'
    'Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'
}]

proxy_https = []
proxy_http = []
ipv4 = ''

choosed_header = {}

city_list = ['西安']

kd_list = []
