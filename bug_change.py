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
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    r = requests.get(url=target,headers=headers)
    r.encoding='utf-8'
    f=open('result.txt','a',encoding='utf-8')
    #f.write(r.text)
    #print(r.text)
    html=etree.HTML(r.text)
    #html_name=html.xpath('/html/body')
    #div[@class="wrap"]/div[@clsaa="book-detail-wrap center990"]/div[@class="book-information cf"]/div[@class="book-info"]/h1/em
    #for i in html_name:
   #     print(i.text)
    name = html.xpath('//title/text()')
    #data=html.xpath('//div[@class="detail"]/p[@class="cf"]/a[@class="blue"]/text()')
    #print(name)
    #name= html.xpath('//div[@class="book-info-detail"]/div[@class="book-state"]/text()')
    data='magnet:.xt=urn:btih:[(0-9)|(A-Z)|(a-z)]{40}'
    result=re.search(data,r.text)
    #print(str(result))
    f.write(str(name)+'\n')
    
    f.write(result.group(0)+'\n')
    
    

def main():
    while(1):
        print("ready")
        url=input()
        #print('url: '+i+'\n')
        
        data_get(url)
    
if __name__ == '__main__':
    main()
