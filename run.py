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

keywords = ['SN-2 PLUS' ,'SN-2' ,'SN2' ,'SN2PLUS' ,'SN2 PLUS' ,'合生元1段奶粉' ,'合生元2段奶粉' ,'合生元3段奶粉' ,'合生元4段奶粉' ,'合生元最新奶粉系列' ,'2015年合生元最新奶粉系列' ,'合生元最新产品系列' ,'2015年合生元最新产品' ,'合生元婴幼儿配方奶粉' ,'合生元孕妇奶粉' ,'合生元呵护奶粉' ,'合生元超级呵护奶粉' ,'合生元金装奶粉系列' ,'合生元超级金装奶粉' ,'奶粉' ,'婴儿奶粉' ,'幼儿奶粉' ,'婴幼儿奶粉' ,'奶粉排行榜' ,'奶粉排行榜10强' ,'奶粉排行榜十强' ,'婴幼儿奶粉排行' ,'婴幼儿奶粉排行榜' ,'婴幼儿奶粉排名' ,'婴幼儿奶粉品牌' ,'婴幼儿奶粉十大品牌' ,'婴儿奶粉质量排行榜' ,'婴儿奶粉排行榜10强' ,'新生儿奶粉排行榜' ,'进口奶粉' ,'进口奶粉排行榜10强' ,'原装进口奶粉排行榜' ,'进口奶粉排行榜' ,'孕妇奶粉排行榜10强' ,'进口奶粉什么牌子好' ,'孕妇吃什么奶粉最好' ,'孕妇喝什么奶粉最好' ,'孕妇奶粉有必要喝吗' ,'宝宝不吃奶粉怎么办' ,'宝宝换奶粉注意事项' ,'宝宝不喝奶粉怎么办' ,'不易上火的奶粉' ,'诺曼底' ,'诺曼底奶源' ,'法国诺曼底' ,'法国诺曼底奶源' ,'奶粉' ,'婴儿奶粉' ,'幼儿奶粉' ,'婴幼儿奶粉' ,'奶粉排行榜' ,'奶粉排行榜10强' ,'奶粉排行榜十强' ,'婴幼儿奶粉排行' ,'婴幼儿奶粉排行榜' ,'婴幼儿奶粉排名' ,'婴幼儿奶粉品牌' ,'婴幼儿奶粉十大品牌' ,'婴儿奶粉质量排行榜' ,'婴儿奶粉排行榜10强' ,'新生儿奶粉排行榜' ,'进口奶粉' ,'进口奶粉排行榜10强' ,'原装进口奶粉排行榜' ,'进口奶粉排行榜' ,'孕妇奶粉排行榜10强' ,'进口奶粉什么牌子好' ,'孕妇吃什么奶粉最好' ,'孕妇喝什么奶粉最好' ,'孕妇奶粉有必要喝吗' ,'宝宝不吃奶粉怎么办' ,'宝宝换奶粉注意事项' ,'宝宝不喝奶粉怎么办' ,'不易上火的奶粉' ,'诺曼底' ,'诺曼底奶源' ,'法国诺曼底' ,'法国诺曼底奶源' ,'什么奶粉好' ,'什么奶粉最好' ,'什么奶粉最好最安全' ,'什么奶粉比较好' ,'什么样的奶粉最好' ,'什么牌子奶粉好' ,'什么牌子的奶粉好' ,'什么牌子奶粉最好' ,'什么牌子的奶粉最好' ,'什么婴儿奶粉最好' ,'奶粉什么牌子好' ,'婴儿奶粉什么牌子好' ,'婴儿奶粉哪个牌子好' ,'婴儿吃什么奶粉好' ,'婴儿喝什么奶粉好' ,'婴儿喝什么奶粉最好' ,'新生儿喝什么奶粉好' ,'新生儿吃什么奶粉好' ,'新生儿喝什么牌子的奶粉好' ,'宝宝喝什么奶粉好' ,'宝宝吃什么奶粉好' ,'宝宝吃什么奶粉最好' ,'宝宝喝什么牌子的奶粉好' ,'刚出生的宝宝吃什么奶粉好' ,'小孩吃什么奶粉最好' ,'美赞臣奶粉怎么样' ,'美赞臣的奶粉怎么样' ,'美赞臣奶粉好吗' ,'美赞臣奶粉上火吗' ,'美赞臣奶粉是哪个国家的' ,'惠氏启赋价格' ,'惠氏启赋奶粉多少钱' ,'惠氏启赋上火吗' ,'惠氏启赋奶粉上火吗' ,'惠氏启赋好吗' ,'惠氏启赋奶粉好吗' ,'惠氏启赋奶粉怎样' ,'惠氏启赋的奶粉怎么样' ,'惠氏启赋2段奶粉怎么样' ,'惠氏启赋奶粉质量好吗' ,'惠氏启赋奶粉产地' ,'惠氏启赋奶粉奶源' ,'诺优能奶粉怎么样' ,'白金诺优能怎么样' ,'诺优能奶粉好不好' ,'诺优能奶粉上火吗' ,'诺优能奶粉有问题吗' ,'美素佳儿奶粉怎么样' ,'美素佳儿的奶粉怎么样啊' ,'美素佳儿奶粉好吗' ,'美素佳儿奶粉到底好不好' ,'美素佳儿婴儿1段奶粉好吗' ,'美素佳儿3段奶粉好吗' ,'美素佳儿孕妇奶粉怎么样' ,'美素佳儿奶粉原产地' ,'美赞臣' ,'惠氏启赋' ,'诺优能' ,'美赞臣奶粉' ,'惠氏启赋奶粉' ,'美素佳儿' ,'荷兰美素佳儿奶粉']
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
            url = get_real_url(o[2])
            title = deal_title(o[3])
            
            if '%s的最新相关信息' % unquote(keyword) in title:
                for o_ in get_news(text):
                    rank = i
                    url =  get_real_url(o_[1])
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
            url = get_real_url(o[0])
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
    m_ = []
    if m:
        txt = m[0][0]
        p = '<div class="(c-gap-bottom-small|c-row)">.*?<a href="(.*?)".*?>(.*?)</a>.*?</div>'
        m_ = re.findall(p, txt, re.S)

    return m_

def get_mobile_news(txt, keyword):
    p = '(<div class=".*?" data-title=\"%s\">(.*?)<div class="result)' % unicode(unquote(keyword))
    m = re.findall(p, txt, re.S)
    m_ = [] 
    if m:
        txt = m[0][1]
        p = '<a href="(.*?)".*?>.*?<p class="\w+">(.*?)</p>.*?</a>'
        m_ = re.findall(p, txt, re.S)

    return m_

def get_real_url(url):
    print '开始获取真实 url：%s' % url
    try:
        r = requests.get(url, timeout=20)
        url = r.url
    except:
        with open('err.txt', 'w') as f:
            msg = '获取真实 url 错误:%s\n' % url
            print msg
            f.write(msg)

    print url
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
