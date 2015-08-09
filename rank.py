#!/usr/bin/env python
#coding: utf-8

import requests
import re
import json
from urllib import unquote
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

keywords = [
        ('向日葵传媒', 'sunflowercn.com/'),
        ('向日葵传媒', 'xrkmedia.com'),
]

keywords = map(lambda x: (repr(x[0]).replace(r'\x', '%')[1:-1], x[1]), keywords)

PAGE_COUNT = 5

HEADER = '关键字,排名\n'

PC_URL = 'http://www.baidu.com/s?wd=%s&pn=%s0'
MOBILE_URL = 'http://m.baidu.com/s?word=%s&&pn=%s0'


def run():
    if not os.path.exists("html_rank"):
        os.mkdir('html_rank')

    print '开始爬取PC端'
    with open('PC_rank.csv', 'w+') as f:
        f.write(HEADER)
        for k in keywords:
            print '爬取关键字：%s' % unquote(k[0])
            f.write(run_pc(k))
            print '爬取内容写入文件完成\n\n'


    print '开始爬取手机端'
    with open('mobile_rank.csv', 'w+') as f:
        f.write(HEADER)
        for k in keywords:
            print '爬取关键字：%s' % unquote(k[0])
            f.write(run_pc(k))
            print '爬取内容写入文件完成\n\n'

def run_pc(keyword):
    for page in range(PAGE_COUNT):
        print '开始获取第%s页内容' % str(page + 1)
        r = requests.get(PC_URL % (keyword[0], page))
        text = r.text
        save_to_file = 'html_rank/pc_%s_page_%s.html' % (unquote(keyword[0]), page + 1)
        print '网页保存至：%s' % save_to_file
        write(text, save_to_file)

        for i, o in enumerate(parse_pc(text)):
            url = get_real_url(o[2])
            
            print url
            if keyword[1] in url:
                tmp = '%s,%s\n' % (unquote(keyword[0]), (page * 10) + i + 1)
                return tmp


    print '没有找到\n'
    return '%s,%s\n' % (unquote(keyword[0]), 0)
 
        

def run_mobile(keyword):
    for page in range(PAGE_COUNT):
        print '开始获取第%s页内容' % str(page + 1)
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53'}
        r = requests.get(MOBILE_URL % (keyword[0], page), headers=headers)
        text = r.text
        save_to_file = 'html_rank/mobile_%s_page_%s.html' % (unquote(keyword[0]), page + 1)
        print '网页保存至：%s' % save_to_file
        write(text, save_to_file)

        for i, o in enumerate(parse_mobile(text)):
            url = o[0].replace('&amp;', '&')

            if keyword[1] in url:
                tmp = '%s,%s\n' % (unquote(keyword[0]), (page * 10) + i + 1)

                return tmp

    return '%s,%s\n' % (unquote(keyword[0]), 0)


def parse_pc(txt):
    p = '<h3 class="(t|t c-gap-bottom-small)">.*?<a.*?(data-click|).*?href\s?=\s?"(.*?)".*?>(.*?)<\/a>.*?<\/h3>'
    return re.findall(p, txt, re.S)

def parse_mobile(txt):
    p = '<div class="result.*?".*?>.*?<a.*?href="(.*?)".*?>(.*?)</a>'
    m = re.findall(p, txt, re.S)
    return m


def get_real_url(url):
    try:
        r = requests.get(url, timeout=20)
        url = r.url
    except:
        pass

    return url


def print_utf8(s):
    print '>>>', json.dumps(s, encoding="UTF-8",  ensure_ascii=False)


def write(s, filename):
    with open(filename, 'w+') as f:
        f.write(s)


def deal_title(title):
    '''
    处理标题
    替换html字符
    处理空格
    处理逗号
    '''
    if title:
        title = title.strip()

        filter_list = ['<em>', '</em>', ',']
        for s in filter_list:
            title = title.replace(s, '')

    return title
    

if __name__ == '__main__':
    run()
