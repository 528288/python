
import requests
import re
from lxml import etree
from bs4 import BeautifulSoup
#读取url列表
def file_read(path):
    update_list=[]
    file=open(path,'r')
    while 1:
        url=file.readline()
        if not url:
            break
        update_list.append(url)
    return update_list

def data_get(target):
    headers = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
    r = requests.get(url=target,headers=headers)
    html=etree.HTML(r.text)
    #html_name=html.xpath('/html/body')
    #div[@class="wrap"]/div[@clsaa="book-detail-wrap center990"]/div[@class="book-information cf"]/div[@class="book-info"]/h1/em
    #for i in html_name:
   #     print(i.text)
    name = html.xpath('//div[@class="book-info "]/h1/em/text()')
    
    data=html.xpath('//div[@class="detail"]/p[@class="cf"]/a[@class="blue"]/text()')
    print("  ".join(name)+"   "+" ".join(data))

    

def main():
    url_list=file_read('url.txt')
    for i in url_list:
        #print('url: '+i+'\n')
        data_get(i)
    a=input()
if __name__ == '__main__':
    main()
