#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import json


def get_url():
    ''' 从 url.txt 中获取要查询的 url 地址 '''
    with open('url.txt', 'r') as f:
        for line in f.xreadlines():
            yield line


def get_html(url):
    ''' 获取页面 html 内容 '''
    url = 'http://baidurank.aizhan.com/baidu/{url}/'.format(url=url)
    r = requests.get(url)
    if r.status_code == 200:
        return r.text


def get_from(html):
    ''' 获取来路 '''
    p = '<span class="red">\d+ ~ (\d+)</span>IP'
    m = re.findall(p, html)

    if m:
        ret = m[0]
    else:
        ret = None
    return ret


def get_total(html, domain):
    ''' 获取总收录数 '''
    p = "url:'http://www.aizhan.com/ajaxAction/shoulu3.php',.*?success"
    m = re.findall(p, html, re.S)
    if m:
        html = m[0]
        p_ = "data:{.*?cc:'(.*?)',rn:'(.*?)'},"
        m_ = re.findall(p_, html)
        if m_:
            cc = m_[0][0]
            rn = m_[0][1]

            data = dict(domain=domain, cc=cc, rn=rn)
            url = 'http://www.aizhan.com/ajaxAction/shoulu3.php?domain={domain}&cc={cc}&rn={rn}'.format(**data)
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text).get('baidu_0days', 0)


def get_word_count(html, domain):
    ''' 获取总词数 '''
    p = 'url:"http://baidurank.aizhan.com/api/wordlocation",.*?success'
    m = re.findall(p, html, re.S)

    pcwl = None
    mwl = None
    if m:
        html = m[0]
        p_ = "data:{.*?ajaxKey:'(.*?)',rn:'(.*?)'},"
        m_ = re.findall(p_, html)
        if m_:
            ajaxKey = m_[0][0]
            rn = m_[0][1]

            data = dict(domain=domain, ajaxKey=ajaxKey, rn=rn)
            url = 'http://baidurank.aizhan.com/api/wordlocation?domain={domain}&ajaxKey={ajaxKey}&rn={rn}'.format(**data)
            r = requests.get(url)
            if r.status_code == 200:
                data = json.loads(r.text)
                pcwl = data.get('pcWL')[0]
                mwl = data.get('mWL')[0]

    return pcwl, mwl


def get_data(html, url):
    ''' 获取需要的 html 块 '''
    p = '<td class="tablehead">(.*?)</td>(.*?)</td>'
    m = re.findall(p, html, re.S)

    pc = None
    mobile = None
    title = None
    for o in m:
        if len(o) == 2:
            title = o[0].encode('utf-8')
            if title == '(PC端)来路':
                pc = get_from(o[1])
            elif title == '(移动)来路':
                mobile = get_from(o[1])

    total = get_total(html, url)
    if total:
        total = total.replace(',', '')
    pcwl, mwl = get_word_count(html, url)

    return dict(url=url, pc=pc, mobile=mobile, total=total, pcwl=pcwl, mwl=mwl)


def main():
    with open('weight.csv', 'w+') as f:
        f.write('url pc 来路,移动来路,总收录,pc 总词数,移动总词数\n')
        for url in get_url():
            url = url.replace('\n', '').replace('\r', '')
            html = get_html(url)
            s = '{url},{pc},{mobile},{total},{pcwl},{mwl}\n'
            if html:
                print s.format(**get_data(html, url))
                f.write(s.format(**get_data(html, url)))


if __name__ == '__main__':
    main()
