from bs4 import BeautifulSoup
from selenium import webdriver
import re
import json
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

#墊腳石
base_url = 'https://www.tcsb.com.tw/?lang=zh-TW'
#for python
#https://www.tcsb.com.tw/v2/Search?q=python&shopId=32014

def GetPag(url):
    tar = url
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(tar)
    for i in range(1000):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        driver.implicitly_wait(5)
    return driver.page_source

#取得書名
def GetBookName(tex):
    soup = BeautifulSoup(tex, 'html.parser')
    course_title = soup.find_all('h5', 'book-title')
    return course_title

#取得連結
def GetBookurl(tex):
    soup = BeautifulSoup(tex, 'html.parser')
    half_url = soup.find_all('a', 'clearfix')
    return half_url

#取得價錢
def GetPrice(tex):
    soup = BeautifulSoup(tex, 'html.parser')
    course_price = soup.find_all('p', 'pull-right price')
    return course_price

#取得出版日期
def GetTime(tex):
    soup = BeautifulSoup(tex, 'html.parser')
    course_time = soup.find_all('p', 'pull-left')
    return course_time


#取得作者
def GetAuthor(tex):
    soup = BeautifulSoup(tex, 'html5lib')
    course_author = soup.find_all('p', 'text-nowrap-ellipsis name')
    return course_author

def GetStuNum(tex):
    soup = BeautifulSoup(tex, 'html.parser')
    course_student_number = soup.find_all('p', 'pull-right person')
    stunumtex = []
    stunumtex2 = []
    number = []
    for x in range(len(course_student_number)):
        stunumtex.append(course_student_number[x].text)
    for x in range(len(course_student_number)):
        stunumtex2.append(stunumtex[x].replace(',', ''))
    for z in range(len(course_student_number)):
        try:
            number.append(re.findall(r"\d+", stunumtex2[z])[0])
        except ValueError:
            print("fail")
            print(number)
    return number



def main():
    url = 'https://www.kingstone.com.tw'
    page = GetPag(url)
    inf = []
    title = GetCouName(page)
    url = GetCouurl(page)
    number = GetStuNum(page)
    price = GetPrice(page)
    author = GetAuthor(page)
    for v in range(len(title)):
        a = title[v].text
        b = url[v]['href']
        b = base_url + b
        c = number[v]
        d = price[v].text
        d = d.replace('\n', '').replace(' ', '')
        e = author[v].text
        inf.append({'title': a, 'url': b, 'number': c, 'price': d, 'author': e})
    for x in inf:
        print(x)
    with open('goldpython.json', 'w', encoding='utf-8') as f:
        json.dump(inf, f, indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    main()