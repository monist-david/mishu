import requests
import re
import json

page = 1  # 最终代码改成for循环可以遍历下载

path = 'https://rate.tmall.com/list_detail_rate.htm?itemId=605164477816&spuId=1383938871&sellerId=3433213584&order=3' \
       '&currentPage='
url = path + str(page)  # 原始链接加上页面
url = 'https://rate.taobao.com/feedRateList.htm?auctionNumId=591224049190&userNumId=1088214634&currentPageNum=1'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4147.135 '
                  'Safari/537.36 Edg/85.0.564.30',
    # referer随便填个淘宝网页应该都能用
    'referer': 'https://detail.tmall.com/item.htm?spm=a230r.1.14.1.23b670a7hhZGQv&id=605164477816&ns=1&abbucket=5',

    'cookie': 'hng=US%7Czh-CN%7CUSD%7C840; t=01b70a49c52cf2ccac861f376c20d22c; _tb_token_=e93be53be93ee; '
              'cookie2=1281bca66d3ed9cb892f39996532b9fd; dnk=monist_d; '
              'uc1=cookie14=UoTV6yz5HHqEFQ%3D%3D&pas=0&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&cookie15=WqG3DMC9VA'
              'QiUQ%3D%3D&existShop=false&cookie21=UIHiLt3xThH8t7YQouiW; uc3=lg2=VFC%2FuZ9ayeYq2g%3D%3D&nk2=Dl9P0Uk3mNU'
              '%3D&vt3=F8dCufTGvFvTIDDpvJc%3D&id2=UNN%2F7XkT7RHQhQ%3D%3D; tracknick=monist_d; lid=monist_d; uc4=nk4=0%4'
              '0DDrKc1vqgeTyOXijpAWU9ub8vw%3D%3D&id4=0%40UgQ3Ak6OOKimNRi7KIblIXJPeUwJ; lgc=monist_d; sgcookie=EiQcm1G2'
              'OvwzMACr9UnrI; csg=c50f876d; enc=MtH67LCYL2NakVGt8KjSWLwAMblK%2F4rzww3iRd5Lv81lQ9shrY1IuqTv71dOIH8%2FHrB'
              'K0cJv6RWTpGr28o9i9Q%3D%3D; cna=GpG4F96ZpRkCAUfonQWHzleJ; _m_h5_tk=9237aef48dd4549d9846bfddd5be4c79_'
              '1598116438889; _m_h5_tk_enc=32aa4fb7033c14c2ffc03942bfbc5f87; xlly_s=1; '
              '_fbp=fb.1.1598367398807.761474013; '
              ' tfstk=c-yVBQ1WktB2xwD19xMwC54iH2LAZYliTLoti5VSQTekTjhcidLtqD9-4D3dEjf..; '
              'l=eBMDzShrOMV3CP_hBOfwourza77OSIRAguPzaNbMiOCPOk5w5hoRWZP7xOTeC3MNh6bXR3-WSGYuBeYBqnV0x6aNa6Fy_Ckmn; '
              'isg=BMnJKJCV8j29ro47KuBztST32PUjFr1IvxRpOGs-RbDssunEs2bNGLfk9A4E6lWA'
}
res = requests.get(url, headers=headers)
print(res.text)

js_str = re.search('\{.*}', res.text)
js_str.group()

js_dict = json.loads(js_str.group())

rateContent = []  # 评论
auctionSku = []  # 款式
rateDate = []  # 时间
for i in range(len(js_dict['rateDetail']['rateList'])):
    rateContent.append(js_dict['rateDetail']['rateList'][i]['rateContent'])
    auctionSku.append([js_dict['rateDetail']['rateList'][i]['auctionSku']])
    rateDate.append([js_dict['rateDetail']['rateList'][i]['rateDate']])

print(rateContent)