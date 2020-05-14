# -*- coding: utf-8 -*-
# @Author: Sam Zhang
# @Date:   2020-04-10 20:05:19
# @Last Modified by:   Sam Zhang
# @Last Modified time: 2020-05-06 16:43:46

import requests
from pprint import pprint as print
from bs4 import BeautifulSoup
import re, os
from urllib.parse import urlparse, quote

# 从output.html中加载备用代码
source = open('./output.html', 'r').read()

def baidu_search(word, pn=0):
    """Crawl Baidu's search results

    Arguments:
        word {str} -- [the search keyword]

    Keyword Arguments:
        pn {int} -- [the search result page number] (default: {0})

    Returns:
        [list, int] -- [returns the search result and the total page num]
    """
    # Set headers
    # Here it's very hard to crawl, and finally I found out it's just a referer's fault
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0",
        "Cookie": "BAIDUID=CA1B0D62CF89B4C908E16806198A988D:SL=0:NR=10:FG=1; BIDUPSID=CA1B0D62CF89B4C908E16806198A988D;\
         PSTM=1584624944; H_PS_PSSID=30969_1436_31125_21112_30908_30824_31086_26350; BD_UPN=133252; BDORZ=B490B5EBF6F3C\
         D402E515D22BCDA1598; BDUSS=VWMFhxZE4wYW02bm02eUg2VDBSTE9za2FxMUtIMzBldWdFbXZhLS1kelJBNXRlRVFBQUFBJCQAAAAAAAAAA\
         AEAAAAPCkwAZGF5ZGF5dXAwNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANF2c17RdnNeNX;\
          H_PS_645EC=3b3f3gvvjx4IBDHqSg1Nic0L7akGB8QRaOAqpSyohTLWY37qsmezLAjZFtZy6oLxvV5T; delPer=0; BD_CK_SAM=1; PSINO\
          =2; COOKIE_SESSION=1138_0_1_1_1_0_0_0_1_0_0_0_1584667911_0_2_0_1584669045_0_1584669043%7C3%230_0_1584669043%7\
          C1; rsv_jmp_slow=1584669520051; ZD_ENTRY=bing; BD_HOME=1; sug=3; sugstore=0; ORIGIN=0; bdime=0; BDRCVFR[feWj1\
          Vr5u3D]=I67x6TjHwwYf0",
        "Referer": "https://www.baidu.com",
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,en-US;q=0.7,zh;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    # Get response
    text = quote(word, 'utf-8')
    url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&ch=&tn=baidu&bar=&wd=%s&rn=&fenlei=256&oq=&rqlang=cn&pn=%d' % (text, pn*10)
    response = requests.get(url,
                            headers=headers)
    # text is the source code after utf-8 encoding
    text = bytes(response.text, response.encoding).decode('utf-8')
    # Create the BeautifulSoup object
    soup = BeautifulSoup(text, 'html.parser')
    try:
        num = int(str(soup.find('span', class_='nums_text').text).strip('百度为您找到相关结果约').strip('个').replace(',', ''))
    except:
        num = 0
    calc = soup.find('div', class_='op_new_cal_screen')
    pre_results = []
    _related = soup.find('div', id='rs').find('table').find_all('th')
    related = []
    for _ in _related:
        if _.text:
            related.append(dict(text=_.text, url='/baidu/s/?q=%s' % quote(_.text, 'utf-8')))
    # print(related)
    if num != 0:
        pre_results.append(dict(type='total', result=num))
    if calc:
        pre_results.append(dict(type='calc', process=str(calc.find('p', class_='op_new_val_screen_process').find('span').text), result=str(calc.find('p', class_='op_new_val_screen_result').find('span').text)))
    if related:
        pre_results.append(dict(type='related', results=related))
    # print(pre_results)
    # source = soup.prettify()
    # with open('./test.html', 'w') as f:
    #     f.write(soup.prettify())
    # Get the main content
    try:
        soup = BeautifulSoup(soup.find_all(id='content_left')[0].prettify(), 'html.parser')
    except IndexError:
        return []
    # Get the results container
    results = soup.find_all(class_='c-container')
    res = []  # The result list
    # Loop over ever result
    for result in results:
        # Create another soup object
        soup = BeautifulSoup(result.prettify(), 'html.parser')
        # Find the link
        href = soup.find_all('a', target='_blank')[0].get('href')
        # And the title
        title = soup.find_all('a', target='_blank')[0].text
        # Get rid of all the html tags
        pattern = re.compile(r'<[^*>]+>', re.S)
        title = pattern.sub('', title)
        # Remove extra lines
        title = title.replace('\n', '')
        try:
            # Find the description
            des = soup.find_all('div', class_='c-abstract')[0].text
            # Yeah, another soup...
            soup = BeautifulSoup(result.prettify(), 'html.parser')
            # Remove html tags
            des = pattern.sub('', des)
            # And remove extra lines and the annoying `\xa0`
            des = des.replace('\n', '').replace('\xa0', '')
        except IndexError:
            try:
                des = des.replace('\n', '')
            except (UnboundLocalError, AttributeError):
                des = None
        # To get the real link, we have to get to the website first
        # Because baidu encodes its search result's link
        if href is not None:
            try:
                r = requests.get(href, timeout=1)
                href = r.url
            except:
                href = href
            if href:
                parse = urlparse(href)
                domain = parse.netloc
                prepath = parse.path.split('/')
                path = []
                for loc in prepath:
                    if loc != '':
                        path.append(loc)
            else:
                domain = None
                path = None
        # Append the result to list
        res.append(dict(title=title, des=des, link=href, domain=domain, path=path))
    # Find the total pages
    soup = BeautifulSoup(text, 'html.parser')
    soup = BeautifulSoup(soup.find_all('div', id='page')[0].prettify(), 'html.parser')
    pages = soup.find_all('span', class_='pc')
    # Return results
    return res, len(pages), pre_results


def google_search(word, pn=0):
    """爬取Google的搜索结果"""
    try:
        pn *= 10
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Host': 'www.google.com',
            'Accept-Language': 'en-US,zh-CN;q=0.7,zh;q=0.3',
            'Referer': 'https://www.google.com/',
            'Proxy-Authorization': 'Basic LnN2QDQxNTAwMTc7Y24uOk45VUc4VXlnVWFRZEEvbkk0VGE4NzJ3QVFhTFl4Sk1pSnRBdnJVNW1vdFlhQmxDME1Va3pVQT09',
            'Connection': 'keep-alive',
            'Cookie': '1P_JAR=2020-04-12-03; NID=202=LZC5lGobjE9m4AUc7EmdIlozoH76L2fTGpDk5k7JSpkf8qTMu9qo0cmqR80EcJC1X7pUcVH9bMjp0TbVVr876NoOrZB8xJFewixpiDus7vt_6-FKuq4V33CVT6zpik5YeHXs-0rH1UOHnrLaTIN_putw8EoVyuWKdNBMA3he2eA; ANID=AHWqTUkte1QyXfU1pEo455Ikdry_2H-zCcu-to8jPpNFmMLedJ_or2KaDeTx2Hrl; DV=I0RsgxQCLlsu0J-HU_sc0eei4UnIFpf9oYQs_p7gJQEAAAA',
            'Content-Length': '0'
        }
        response = requests.get('https://www.google.com/search?q=%s&start=%d' % (word, pn), headers=headers)
        text = str(bytes(response.text, response.encoding).decode('utf-8'))
        # 如果你无法访问Google，可以注释掉上面的代码，换做下面的，它从output.html里加载代码
        # output.html中是Google对hello的搜索结果的第一页的源码，所以如果使用它的话搜什么都是一个结果
        # text = source
        soup = BeautifulSoup(text, 'html.parser')
        results = []
        i = 0
        try:
            for g in soup.find_all('div', class_='r'):
                anchors = g.find_all('a')
                if anchors:
                    link = anchors[0]['href']
                    title = g.find('h3').text
                    soup2 = BeautifulSoup(str(text), 'html.parser')
                    soup2 = BeautifulSoup(str(soup2.findAll('div', class_='s')[i]), 'html.parser')
                    des = soup2.find('span', class_='st').text
                    if link:
                        parse = urlparse(link)
                        domain = parse.netloc
                        prepath = parse.path.split('/')
                        path = []
                        for loc in prepath:
                            if loc != '':
                                path.append(loc)
                    else:
                        domain = None
                        path = None
                    item = {
                        'title': title,
                        'link': link,
                        'des': des,
                        'domain': domain,
                        'path': path
                    }
                    results.append(item)
                    i += 1
        except:
            pass
        nav = soup.find('div', id='foot')
        soup2 = BeautifulSoup(str(nav), 'html.parser')
        soup2 = BeautifulSoup(str(soup2.find('span', id='xjs')), 'html.parser')
        soup2 = BeautifulSoup(str(soup2.find('table')), 'html.parser')
        nav = soup2.findAll('td')
        pages = []
        for i in nav:
            try:
                pages.append(int(i.text))
            except ValueError:
                pass
        return [results, pages]
    except:
        return [[], []]


def get_version():
    return os.environ.get('CURRENT_VERSION', '1.0')


if __name__ == '__main__':
    print(baidu_search('1+1'))
