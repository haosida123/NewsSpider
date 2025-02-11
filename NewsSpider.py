# -*- coding: utf-8 -*-
import os
# import sys
# import urllib2
import requests
import re
from lxml import etree


def StringListSave(save_path, filename, slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path+"/"+filename+".txt"
    with open(path, "w+", encoding='utf-8') as fp:
        for s in slist:
            # fp.write("%s\t\t%s\n" % (s[0].encode("utf8"), s[1].encode("utf8")))
            if len(s) == 2:
                fp.write("%s\t\t%s\n" % (s[0], s[1]))
            else:
                fp.write("%s\t\t%s\t\t%s\n" % (s[0], s[1], s[2]))

def Page_Info(myPage):
    '''Regex'''
    mypage_Info = re.findall(r'<div class="titleBar" id=".*?"><h2>(.*?)</h2><div class="more"><a href="(.*?)">.*?</a></div></div>', myPage, re.S)
    return mypage_Info

def New_Page_Info(new_page):
    '''Regex(slowly) or Xpath(fast)'''
    # new_page_Info = re.findall(r'<td class=".*?">.*?<a href="(.*?)\.html".*?>(.*?)</a></td>', new_page, re.S)
    # # new_page_Info = re.findall(r'<td class=".*?">.*?<a href="(.*?)">(.*?)</a></td>', new_page, re.S) # bugs
    # results = []
    # for url, item in new_page_Info:
    #     results.append((item, url+".html"))
    # return results
    dom = etree.HTML(new_page)
    new_items = dom.xpath('//tr/td/a/text()')
    new_urls = dom.xpath('//tr/td/a/@href')
    assert(len(new_items) == len(new_urls))
    sub_pages = []
    for new_url in new_urls:
        try:
            sub_page = requests.get(new_url).content.decode("gb18030", 'ignore')
            sub_dom = etree.HTML(sub_page)
            sub_pages.append(sub_dom.xpath('//div[@class="post_text"]/p/text()'))
        except Exception as e:
            continue
    # print(sub_item)
    return zip(new_items, new_urls, sub_pages)

def Spider(url):
    i = 0
    print("downloading ", url)
    myPage = requests.get(url).content.decode("gbk")
    # myPage = urllib2.urlopen(url).read().decode("gbk")
    myPageResults = Page_Info(myPage)
    save_path = u"网易新闻抓取"
    filename = str(i)+"_"+u"新闻排行榜"
    StringListSave(save_path, filename, myPageResults)
    i += 1
    for item, url in myPageResults:

        if i<9: i+=1; continue

        print("downloading ", url)
        new_page = requests.get(url).content.decode("gbk")
        # new_page = urllib2.urlopen(url).read().decode("gbk")
        newPageResults = New_Page_Info(new_page)
        filename = str(i)+"_"+item
        StringListSave(save_path, filename, newPageResults)
        i += 1


if __name__ == '__main__':
    print("start")
    start_url = "http://news.163.com/rank/"
    Spider(start_url)
    print("end")
