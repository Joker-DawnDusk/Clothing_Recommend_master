import requests
from bs4 import BeautifulSoup
import unicodedata
import logging
import csv
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# options = Options()
# options.add_argument('--headless')                       # 无头模式 后台运行 不弹出浏览器
# options.add_argument('--disable-gpu')                    # 谷歌文档提到需添加此属性以规避bug
# chrome_driver = 'C:\ProgramData\Anaconda3\chromedriver'  # 谷歌驱动器路径
#
poster_save_path = './poster'
# driver = webdriver.Chrome(options=options, executable_path=chrome_driver)
i = 0
with open('./info/info_2.csv', encoding='utf-8') as fb:
    reader = csv.reader(fb)
    reader.__next__()
    for line in reader:
        url = line[5]
        unique_id = line[1]
        # driver.get(url)
        # driver.implicitly_wait(10)
        response = requests.get(url)
        with open(f'{poster_save_path}/{unique_id}.jpg', 'wb') as fb:
            fb.write(response.content)
        i = i + 1
        print(i)