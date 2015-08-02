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

keywords = ['天使汇', 'tech2ipo', '羊羊羊']
keywords = map(lambda x: repr(x).replace(r'\x', '%')[1:-1], keywords)

PAGE_COUNT = 2

HEADER = '关键字,页码,排名,标题,链接\n'

PC_URL = 'http://www.baidu.com/s?wd=%s&pn=%s0'
ZHIDAO_URL = 'http://zhidao.baidu.com/search?word=%s&pn=%s0'
MOBILE_URL = 'http://m.baidu.com/s?word=%s&&pn=%s0'

def run():
    
    if not os.path.exists("html"):
        os.mkdir('html')

    print '开始爬取PC端'
    with open('PC.csv', 'w+') as f:
        f.write(HEADER)
        for k in keywords:
            print '爬取关键字：%s' % unquote(k)
            f.write(run_pc(k))
            print '爬取内容写入文件完成\n\n'

    print '开始爬取垂直端'
    with open('zhidao.csv', 'w+') as f:
        f.write(HEADER)
        for k in keywords:
            print '爬取关键字：%s' % unquote(k)
            f.write(run_zhidao(k))
            print '爬取内容写入文件完成\n\n'

    print '开始爬取手机端'
    with open('mobile.csv', 'w+') as f:
        f.write(HEADER)
        for k in keywords:
            print '爬取关键字：%s' % unquote(k)
            f.write(run_mobile(k))
            print '爬取内容写入文件完成\n\n'

def run_pc(keyword):
    s = list()

    for page in range(PAGE_COUNT):
        print '开始获取第%s页内容' % str(page + 1)
        r = requests.get(PC_URL % (keyword, page))
        text = r.text
        save_to_file = 'html/pc_%s_page_%s.html' % (unquote(keyword), page + 1)
        print '网页保存至：%s' % save_to_file
        write(text, save_to_file)

        for i, o in enumerate(parse_pc(text)):
            rank = i 
            url = o[2]
            title = deal_title(o[3])
            
            if '%s的最新相关信息' % unquote(keyword) in title:
                for o_ in get_news(text):
                    rank = i
                    url = o_[1]
                    title = deal_title(o_[2])
                    tmp = '%s,%s,%s,%s,%s\n' % (unquote(keyword), page + 1, i + 1, title, url)
                    s.append(tmp)

            else:
                tmp = '%s,%s,%s,%s,%s\n' % (unquote(keyword), page + 1, i + 1, title, url)
                s.append(tmp)

           
    return ''.join(s)
        
def run_zhidao(keyword):
    s = list()
    for page in range(PAGE_COUNT):
        print '开始获取第%s页内容' % str(page + 1)
        r = requests.get(ZHIDAO_URL % (keyword, page))
        r.encoding = 'gbk'
        text = r.text
        save_to_file = 'html/zhidao_%s_page_%s.html' % (unquote(keyword), page + 1)
        print '网页保存至：%s' % save_to_file
        write(text, save_to_file)

        for i, o in enumerate(parse_zhidao(text)):
            rank = i 
            url = o[0]
            title = deal_title(o[1])
            
            tmp = '%s,%s,%s,%s,%s\n' % (unquote(keyword), page + 1, i + 1, title, url)
            s.append(tmp)

    return ''.join(s)


def run_mobile(keyword):
    s = list()
    for page in range(PAGE_COUNT):
        print '开始获取第%s页内容' % str(page + 1)
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53'}
        r = requests.get(MOBILE_URL % (keyword, page), headers=headers)
        text = r.text
        save_to_file = 'html/mobile_%s_page_%s.html' % (unquote(keyword), page + 1)
        print '网页保存至：%s' % save_to_file
        write(text, save_to_file)

        for i, o in enumerate(parse_mobile(text)):
            rank = i 
            url = o[0].replace('&amp;', '&')
            if not url.startswith('http://m.baidu.com'):
                url = 'http://m.baidu.com/%s' % url
            p = re.compile('<.*?>')
            title = re.sub(p, '==', deal_title(o[1]))
            title = filter(None, title.split('=='))[0]
            
            if title == '下一页':
                continue

            if '%s的相关消息' % unquote(keyword) in title:
                for o_ in get_mobile_news(text, keyword):
                    rank = i
                    url = o_[0]
                    if not url.startswith('http://m.baidu.com'):
                        url = 'http://m.baidu.com/%s' % url
                    title = deal_title(o_[1])
                    tmp = '%s,%s,%s,%s,%s\n' % (unquote(keyword), page + 1, i + 1, title, url)
                    s.append(tmp)

            else:
                tmp = '%s,%s,%s,%s,%s\n' % (unquote(keyword), page + 1, i + 1, title, url)
                s.append(tmp)

    return ''.join(s)


def parse_pc(txt):
    p = '<h3 class="(t|t c-gap-bottom-small)">.*?<a.*?(data-click|).*?href\s?=\s?"(.*?)".*?>(.*?)<\/a>.*?<\/h3>'
    return re.findall(p, txt, re.S)

def parse_zhidao(txt):
    p = '<dt class="dt mb-4 line" alog-alias="result-title-\d+">.*?<a href="(.*?)".*?>(.*?)</a>.*?</dt>'
    m = re.findall(p, txt, re.S)
    return m

def parse_mobile(txt):
    p = '<div class="result.*?".*?>.*?<a.*?href="(.*?)".*?>(.*?)</a>'
    m = re.findall(p, txt, re.S)
    return m

def get_news(txt):
    p = '(<div class="c-offset">(.*?)<div class="result)'
    m = re.findall(p, txt, re.S)
    m_ = None
    if m:
        txt = m[0][0]
        p = '<div class="(c-gap-bottom-small|c-row)">.*?<a href="(.*?)".*?>(.*?)</a>.*?</div>'
        m_ = re.findall(p, txt, re.S)

    return m_

def get_mobile_news(txt, keyword):
    p = '(<div class=".*?" data-title=\"%s\">(.*?)<div class="result)' % unicode(unquote(keyword))
    m = re.findall(p, txt, re.S)
    m_ = None
    if m:
        txt = m[0][1]
        p = '<a href="(.*?)".*?>.*?<p class="\w+">(.*?)</p>.*?</a>'
        m_ = re.findall(p, txt, re.S)

    return m_


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
