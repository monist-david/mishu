import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait
from twisted.conch.telnet import EC

options = Options()
#options.add_argument("--headless")
dirver = webdriver.Firefox(firefox_options=options)
# 初次建立连接, 随后方可修改cookie
dirver.get('http://www.taobao.com')
# 删除第一次登录是储存到本地的cookie
dirver.delete_all_cookies()
# 读取登录时储存到本地的cookie
with open("cookies_tao.json", "r", encoding="utf8") as fp:
    ListCookies = json.loads(fp.read())

for cookie in ListCookies:
    dirver.add_cookie({
        'domain': '.taobao.com',  # 此处xxx.com前，需要带点
        'name': cookie['name'],
        'value': cookie['value'],
        'path': '/',
        'expires': None
    })

# 再次访问页面，便可实现免登陆访问
dirver.get("http://www.taobao.com")
time.sleep(3)
# 将页面保存为图片用于查看是否登录成功
search = dirver.find_element_by_id('q')
search.send_keys("男装")
search.send_keys(Keys.ENTER)
time.sleep(3)
url1 = dirver.current_url
print(dirver.current_url)
dirver.get(url1)
time.sleep(2)
sort = dirver.find_element_by_link_text('销量')
sort.click()
shangpin = dirver.find_element_by_id('J_Itemlist_Pic_565221245456')
shangpin.click()
time.sleep(2)
sreach_windows = dirver.current_window_handle
all_handles = dirver.window_handles
for handle in all_handles:
    if handle != sreach_windows:
        dirver.switch_to.window(handle)
        time.sleep(2)
        ding = dirver.find_element_by_id('J_TabBarBox')
        dirver.execute_script("arguments[0].scrollIntoView()", ding)
        time.sleep(3)
        num = 0
        while num < 10:
            ck = dirver.find_element_by_xpath('//*[@id="J_TabBar"]/li[3]/a')
            ck.click()
            time.sleep(3)
            texts = dirver.find_elements_by_class_name('tm-col-master')
            print(texts)
            for each in texts:
                text = each.find_element_by_class_name('tm-rate-fulltxt')
                print(text.text)
            bbb = dirver.find_element_by_link_text('下一页>>')
            dirver.execute_script("arguments[0].scrollIntoView()", bbb)
            time.sleep(1)
            bbb.send_keys(Keys.ENTER)
            num = num + 1
dirver.quit()
