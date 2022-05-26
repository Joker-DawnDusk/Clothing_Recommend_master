import requests
from bs4 import BeautifulSoup
import unicodedata
import logging
import csv
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

Page_num = 10        # 每种服装需爬取的页面数量
# Id = 0               # 全局服装id

options = Options()
options.add_argument('--headless')                       # 无头模式 后台运行 不弹出浏览器
options.add_argument('--disable-gpu')                    # 谷歌文档提到需添加此属性以规避bug
chrome_driver = 'C:\ProgramData\Anaconda3\chromedriver'  # 谷歌驱动器路径

class Model():
    def __init__(self):
        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        }
        # 服装id
        self.id = 0
        # 存放服装种类
        self.clothes_type = []
        # 存放不同服装种类的response
        self.response_list = []
        # 服装初始url
        self.url = 'https://search.jd.com/Search?'
        # 图片的保存路径
        self.poster_save_path = './poster'
        # 服装信息的保存文件
        self.info_save_path = './info/info.csv'
        # logging的配置，记录运行日志
        logging.basicConfig(filename="cloth.log", filemode="a+", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

    def get_clothes_type(self):
        '''
        获取服装种类
        '''
        with open('./info/genre.txt', encoding='utf-8') as fb:
            for line in fb:
                line = line.strip()
                line = urllib.parse.quote(line)
                self.clothes_type.append(line)

    def get_url_response(self, url, keyword, page):
        '''
        访问网页请求，返回response
        '''
        logging.info(f'get {url}')
        i = 0
        driver = webdriver.Chrome(options=options, executable_path=chrome_driver)
        # 超时重传，最多5次
        while i < 5:
            try:
                driver.get(url + 'keyword=' + str(keyword) + '&enc=utf-8' + '&page=' + str(page))
                driver.implicitly_wait(10)      # 隐式等待 等待网页数据加载完成 网页数据加载完成立即执行下方代码
                # 模拟javascript将滚轮条拉到最底层
                for i in range(1, 12, 2):
                    time.sleep(1)
                    j = i / 9
                    js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
                    driver.execute_script(js)
                if driver:
                    logging.info(f'get {url} sucess')
                    # 正常获取，直接返回
                    return driver
                # 如果状态码不对，获取失败，返回None，不再尝试
                logging.error(f'get {url} status_code error')
                return None
            except:
                # 访问超时
                logging.error(f'get {url} error, try to restart {i + 1}')
                i += 1
        # 重试5次都失败，返回None
        return None

    def get_pic_response(self, url):
        '''
        访问网页请求，返回服装图片response
        '''
        logging.info(f'get {url}')
        i = 0
        # 超时重传，最多5次
        while i < 5:
            try:
                response = requests.get(url, timeout=6)
                if response.status_code == 200:
                    logging.info(f'get {url} sucess')
                    # 正常获取，直接返回
                    return response
                # 如果状态码不对，获取失败，返回None，不再尝试
                logging.error(f'get {url} status_code error: {response.status_code}')
                return None
            except requests.RequestException:
                # 如果超时
                logging.error(f'get {url} error, try to restart {i + 1}')
                i += 1
        # 重试5次都失败，返回None
        return None

    def process_html(self, driver, clothing_type):
        '''
        解析html，获取服装信息
        '''
        soup = BeautifulSoup(driver.page_source, 'lxml')
        items = soup.find_all('li', 'gl-item')
        for item in items:
            # 服装唯一id  如：10045029971637
            unique_id = item.find('div', class_='p-img').a['href'].strip()
            unique_id = unique_id.replace('//item.jd.com/', '')
            unique_id = unique_id.replace('.html', '')
            unique_id = int(unique_id)

            # 服装名字         如：班尼路2022春夏新款潮流抗菌polo衫男休闲简约百搭港风翻领短袖上衣 00A M
            name = item.find('div', class_='p-name').a.em.text.strip()
            # 去掉html的特殊符号
            name = unicodedata.normalize('NFKC', name)
            name = name.replace('\n', '')
            name = name.replace(' ', '')
            name = name.replace('   ', '')

            # 服装图片url
            pic_url = ''
            try:
                if item.find('div', class_='p-img').a.img['data-lazy-img'].strip():
                    pic_url = 'https:' + item.find('div', class_='p-img').a.img['data-lazy-img'].strip()
                    pic_re = self.get_pic_response(pic_url)
                    # 保存图片
                    self.save_poster(unique_id, pic_re.content)
                    pic_re.close()
                else:
                    pass
            except:
                if item.find('div', class_='p-img').a.img['src'].strip():
                    pic_url = 'https:' + item.find('div', class_='p-img').a.img['src'].strip()
                    pic_re = self.get_pic_response(pic_url)
                    # 保存图片
                    self.save_poster(unique_id, pic_re.content)
                    pic_re.close()
                else:
                    logging.error('图片错误')


            # 服装详情页url
            item_url = 'https:' + item.find('div', class_='p-img').a['href'].strip()

            # 服装种类
            item_type = urllib.parse.unquote(clothing_type)

            # 服装店铺名字
            shop = item.find('div', class_='p-shop').span.a.text.strip()

            # 服装价格
            price = '￥' + item.find('div', class_='p-price').strong.i.text.strip()

            # id，服装唯一id，服装名字，服装详情链接，服装图片url，种类，商铺，价格
            self.id = self.id + 1
            detail = [self.id, unique_id, name, item_url, pic_url, item_type, shop, price]
            self.save_info(detail)


    def save_poster(self, unique_id, content):
        # 保存图片
        with open(f'{self.poster_save_path}/{unique_id}.jpg', 'wb') as fb:
            fb.write(content)

    def save_info(self, detail):
        # 存储到CSV文件中
        with open(f'{self.info_save_path}', 'a+', encoding='utf-8', newline='') as fb:
            writer = csv.writer(fb)
            writer.writerow(detail)

    def run(self):
        # 开始爬取信息
        self.get_clothes_type()
        id = 0
        # 根据不同服装种类爬取信息
        for c_type in self.clothes_type:
            # 分页爬取
            for page1 in range(0, Page_num):
                page = page1 * 2 + 1
                driver = self.get_url_response(self.url, keyword=c_type, page=page)
                # 处理服装详情信息
                self.process_html(driver, clothing_type=c_type)
                logging.info(f'process clothes {self.id} success')
        driver.close()


if __name__ == '__main__':
    s = Model()
    s.run()