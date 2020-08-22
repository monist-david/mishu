import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
driver = webdriver.Chrome('C:/Users/david/Desktop/site/django site/mishu/search/chromedriver.exe')
driver.get(
    'https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fbuyertrade.taobao.com%2Ftrade%2Fitemlist%2Flist_bought_items.htm%3Fspm%3D875.7931836%252FB.a2226mz.4.66144265Vdg7d5%26t%3D20110530')
# 这里是为了等待手机扫码登录, 登录后回车即可
input("请回车登录")
dictCookies = driver.get_cookies()
jsonCookies = json.dumps(dictCookies)
# 登录完成后,将cookies保存到本地文件
with open("cookies_tao.json", "w") as fp:
    fp.write(jsonCookies)