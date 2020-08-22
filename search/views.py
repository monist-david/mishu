from .forms import SearchForm
from django.shortcuts import render
from django.views.generic import TemplateView
from selenium.webdriver.common.keys import Keys
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import jieba.analyse
import jieba
import jieba.posseg as pseg
import json


# Create your views here.
class HomeView(TemplateView):
    template_name = "search/search.html"

    def login_and_search(self, keyword):
        print("正在登录")
        driver = webdriver.Chrome('C:/Users/david/Desktop/site/django site/mishu/search/chromedriver.exe')

        # 初次建立连接, 随后方可修改cookie
        driver.get('http://www.taobao.com')
        # 删除第一次登录是储存到本地的cookie
        driver.delete_all_cookies()
        # 读取登录时储存到本地的cookie
        with open("C:/Users/david/Desktop/site/django site/mishu/search/cookies_tao.json", "r", encoding="utf8") as fp:
            ListCookies = json.loads(fp.read())

        for cookie in ListCookies:
            driver.add_cookie({
                'domain': '.taobao.com',  # 此处xxx.com前，需要带点
                'name': cookie['name'],
                'value': cookie['value'],
                'path': '/',
                'expires': None
            })

        # 再次访问页面，便可实现免登陆访问
        driver.get("http://www.taobao.com")
        time.sleep(3)
        wait = WebDriverWait(driver, 20)
        # 需要用手机淘宝扫二维码登录才能搜索
        print("正在查找", keyword)
        try:
            input = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="mq"]'))
            )
            input.send_keys(keyword)
            input.send_keys(Keys.RETURN)
            total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                               "#mainsrp-pager > div > div > div > div.total")))

            print(total.text)
            time.sleep(5)
            return total.text, wait, driver
        except TimeoutError:
            return self.login_and_search(keyword)

    def get_goods(self, wait, driver):
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                       '#mainsrp-itemlist .items '
                                                       '.item')))
            html = driver.page_source
            doc = pq(html)
            items = doc('#mainsrp-itemlist .items .item').items()
            for item in items:
                print('again')
                goods = {
                    'img': item.find('.pic .img').attr('data-src'),
                    'price': item.find('.price').text(),
                    'deal': item.find('.deal-cnt').text(),
                    'title': item.find('.title').text(),
                    'shop': item.find('.shop').text(),
                    'location': item.find('.location').text(),
                    'url': item.find('.pic a').attr('href')
                }
                driver.execute_script("window.open('" + str(goods['url']) + "')")
                sreach_windows = driver.current_window_handle
                all_handles = driver.window_handles
                for handle in all_handles:
                    if handle != sreach_windows:
                        driver.switch_to.window(handle)
                        time.sleep(2)
                        ding = driver.find_element_by_id('J_TabBarBox')
                        print(ding)
                        driver.execute_script("arguments[0].scrollIntoView()", ding)
                        time.sleep(2)
                        driver.execute_script("arguments[0].scrollIntoView()", ding)
                        time.sleep(2)
                        num = 0
                        while num < 10:
                            time.sleep(3)
                            texts = driver.find_elements_by_class_name('tm-col-master')
                            for each in texts:
                                text = each.find_element_by_class_name('tm-rate-fulltxt')
                                print(text.text)
                            print('work')
                            try:
                                bbb = driver.find_element_by_link_text('下一页>>')
                                driver.execute_script("arguments[0].scrollIntoView()", bbb)

                                time.sleep(2)
                                bbb.send_keys(Keys.ENTER)
                                num = num + 1
                            except:
                                print('break')
                                break
                        print(num)
                driver.close()
                driver.switch_to.window(sreach_windows)
                print('num')
        except Exception:
            print("获取商品失败")

    def next_page(self, page_number, wait, driver):
        print("正在换页", page_number)
        try:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
            )
            submit = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"))
            )
            input.clear()
            input.send_keys(page_number)
            submit.click()
            wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                         '#mainsrp-pager > div > ' \
                                                         'div > div > ul > ' \
                                                         'li.item.active > ' \
                                                         'span'), str(page_number)))
            self.get_goods(wait, driver)
        except Exception:
            self.next_page(page_number, wait, driver)

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            # product_price_range_min = form.cleaned_data['product_price_range_min']
            # product_price_range_max = form.cleaned_data['product_price_range_max']
            product_style = form.cleaned_data['product_style']
            product_comment = form.cleaned_data['product_comment']
            print(product_name)
            # print(product_price_range_min)
            # print(product_price_range_max)
            print(product_style)
            print(product_comment)

        # handles = driver.window_handles
        # driver.switch_to.window(handles[-1])

        keyword = input('你要买的是什么商品？')
        demands = input('你用这个商品做什么用？请尽量简洁。')
        jieba.enable_paddle()

        words = pseg.cut(demands, use_paddle=True)  # paddle模式

        for word, flag in words:
            if flag == 'v':
                keyword += word
        total = self.login_and_search(keyword)
        total_1 = int(re.compile('(\d+)').search(total[0]).group(0))
        for i in range(2, total_1 + 1):
            if i % 15 == 0:
                time.sleep(20)
            self.next_page(i, total[1], total[2])

        # products = self.driver.find_elements_by_class_name('J_ItemPic img')
        # for pro in products:
        #     print(pro.text)

        return render(request, self.template_name)
