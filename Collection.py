import requests
from bs4 import BeautifulSoup
from subprocess import Popen
import re

def collections(soup):
    colls = {}
    collcLinks = soup.find_all('div', {'class': 'zm-item'})
    for link in collcLinks:
        each_collc = link.find_all('a')[0]
        colls[each_collc.get_text()] = 'http://www.zhihu.com' + each_collc['href']
    return colls

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Referer": "http://www.zhihu.com/"
    }

def getXSRF():
    resp = requests.get('http://www.zhihu.com')
    return BeautifulSoup(resp.text, 'html.parser').find('input', {'name': '_xsrf'})['value']

def getCaptcha():
    captcha_url = 'http://www.zhihu.com/captcha.gif'
    captcha = requests.get(captcha_url, headers = headers)
    #print(captcha.content)
    with open('captcha.gif', 'wb') as f:
        f.write(captcha.content)
   # Popen('captcha.gif', shell =True)   #在程序中运行其他程序或shell
    captcha = input('captcha: ')
    return captcha

xsrf = getXSRF()
Cap = getCaptcha()

data = {
    'email': '1280119355@qq.com',
    'password': '1280119355',
    'remember_me': 'true',
    '_xsrf': xsrf,
    'captcha': Cap
}

s = requests.session()
r = s.post('http://www.zhihu.com/login/email', headers = headers, data = data)
print(r.text)
print('---------------------------------')

m_cookies = r.cookies

collection_page = s.get('http://www.zhihu.com/collections/mine', headers = headers)
soup = BeautifulSoup(collection_page.text, "html.parser")
print(soup.head.title)

collc = collections(soup)
print(collc)
