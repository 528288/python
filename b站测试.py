import os
#from pickle import APPEND
import re
import argparse
import subprocess
import prettytable
from DecryptLogin import login
import time
import urllib
#import threading   
import requests,json,time
import sys
import chardet
from io import BytesIO
import gzip

'''B站类'''
class Bilibili():
    def __init__(self, username, password, **kwargs):
        #登录b站
        self.username = username
        self.password = password
        self.session = Bilibili.login(username, password)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        }
    
        self.user_info_url = 'https://api.bilibili.com/x/space/acc/info'
        self.submit_videos_url = 'https://api.bilibili.com/x/space/arc/search'
        self.view_url = 'https://api.bilibili.com/x/web-interface/view'
        self.video_player_url = 'https://api.bilibili.com/x/player/playurl'
        self.pagelist_url='https://api.bilibili.com/x/player/pagelist'
        #列出有哪些收藏夹
        self.fold_url='https://api.bilibili.com/x/v3/fav/folder/created/list-all'
        self.foldlist_url='https://api.bilibili.com/x/v3/fav/resource/list'
        # 非会员用户只能下载到高清1080P
        self.quality = [('16', '流畅 360P'), ('32', '清晰 480P'), ('64', '高清 720P'), ('74', '高清 720P60'), ('80', '高清 1080P'), ('112', '高清 1080P+'), ('116', '高清 1080P60')][-3]
        # 获得用户的视频基本信息
        self.video_info = {'aids': [],'bvids':[],'video_nums':[],'cid_parts': [], 'titles': [], 'links': [], 'down_flags': []}
        
        self.out_pipe_quiet = subprocess.PIPE
        self.out_pipe = None
        #默认路径不存在则创建默认路径
        self.save_path='bili_videos'
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)

        
    '''运行主程序'''
    def run(self):
        while True:
            self.video_info = {'aids': [],'bvids':[],'video_nums':[],'cid_parts': [], 'titles': [], 'links': [], 'down_flags': []}
            userid = input('请输入目标用户ID(例:243766613) ——> ')
            #获取up主信息
            user_info = self.__getUserInfo(userid)
            #将获取到的u信息up信息以表格形式输出
            #创建表格
            tb = prettytable.PrettyTable()
            #添加表头
            tb.field_names = list(user_info.keys())
            #按行加入表内容
            tb.add_row(list(user_info.values()))
            print('获取的用户信息如下:')
            #输出表格
            print(tb)
            is_download = input('是否下载该用户的所有视频(y/n, 默认: y) ——> ')
            if is_download == 'y' or is_download == 'yes' or not is_download:
                self.__downloadSpaceVideos(userid)
                

    '''根据userid获得该用户基本信息'''
    def __getUserInfo(self, userid):
        params = {'mid': userid, 'jsonp': 'jsonp'}
        response = self.session.get(self.user_info_url, params=params, headers=self.headers)
        response_json = response.json()
        user_info = {
            '用户名': response_json['data']['name'],
            '性别': response_json['data']['sex'],
            '个性签名': response_json['data']['sign'],
            '用户等级': response_json['data']['level'],
            '生日': response_json['data']['birthday']
        }
        return user_info
    #获取视频信息
    def __getVideoInfo(self,bvid):
        params = {'bvid': bvid}
        response = self.session.get(self.view_url, headers=self.headers, params=params)
        #view_url_response_json=response.json()
        view_url_response_json=response.json()
        cid_part = []
        for page in view_url_response_json['data']['pages']:
        #添加视频的cid及名字,该api中获取的part为bvid下挂载的小视频名字
            cid_part.append([page['cid'], page['part']])
        self.video_info['cid_parts'].append(cid_part)
        self.video_info['video_nums'].append(int(view_url_response_json['data']['videos']))
        #该bvid对应的主标题,
        title = response.json()['data']['title']
        #去除奇怪的中文符号
        title = re.sub(r"[‘’\/\\\:\*\?\"\<\>\|\s']", ' ', title)
        #主集合内添加标题
        self.video_info['titles'].append(title)
    def __setSavePath(self,path):
        self.save_path=r''+path
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)
        
    def __downloadVideo(self,bvid)->bool:
        params = {'bvid': bvid}
        response = self.session.get(self.view_url, headers=self.headers, params=params)
        view_url_response_json=response.json()
        video_nums=int(view_url_response_json['data']['videos'])
        url = 'https://www.bilibili.com/video/{}'.format('%s' %bvid)
        if video_nums>1:
            down_cmd = 'you-get.exe --playlist -o {} {}'
            
        else:
            down_cmd=command = 'you-get.exe -o {} {}'
        down_cmd = down_cmd.format(self.save_path, url)
        process = subprocess.Popen(down_cmd, stdout=self.out_pipe, stderr=self.out_pipe, shell=True)
        try:
            process.wait()
            return True
        except:
            return False
            
 
    
    '''下载目标用户的所有视频'''
    def __downloadSpaceVideos(self, userid):
        if not os.path.exists(userid):
            os.mkdir(userid)
        
        params = {'keyword': '', 'mid': userid, 'ps': 30, 'tid': 0, 'pn': 1, 'order': 'pubdate'}
        while True:
            response = self.session.get(self.submit_videos_url, headers=self.headers, params=params)
            response_json = response.json()
            for item in response_json['data']['list']['vlist']:
                #self.video_info['aids'].append(item['aid'])
                self.video_info['bvids'].append(item['bvid'])
            if len(self.video_info['bvids']) < int(response_json['data']['page']['count']):
                params['pn'] += 1
            else:
                break
        #遍历视频
        
        for bvid in self.video_info['bvids']:
            self.__getVideoInfo(bvid)
            
        print('共获取到用户ID<%s>的<%d>个视频...' % (userid, len(self.video_info['titles'])))
        #沉默调用命令行
        for idx in range(len(self.video_info['titles'])):
            #获取bv号
            down_bvid = self.video_info['bvids'][idx]
            #调用下载函数
            self.__downloadVideo(down_bvid)
            try:
                self.getVideoSrt(down_bvid)
            except:
                print("%s 字幕下载失败"%down_bvid)
                
        '''
        aria2c_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'tools/aria2c')
        ffmpeg_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'tools/ffmpeg')
        
   
       '''
        #下载字幕文件
    def getVideoSrt(self,bvid):
        self.ergodBvid(bvid)
    
    def ergodBvid(self,bvid):
        bvid_dict = self.__pn(bvid)
        #print(bvid_dict)
        p = len(bvid_dict['data'])            
        i = 0                      #计数器
        while i<p:                 #循环多P视频
            cid = bvid_dict['data'][i]['cid']              #获取该P视频的cid
            i += 1                             #计数器+1
            self.__xiaZaiDanPZiMu(bvid,cid,i,bvid_dict)           #下载该P视频的字幕
            print ('【任务总进度：%s/%sP】\n'%(i,p))   #汇报任务进度（以P算）
            print ('\n\n*** 任务完成 ***\n')    #最终完成报告

    def __xiaZaiDanPZiMu(self,aid,cid,p,my_bvid_dict):#根据cid下载该P视频内的全部字幕（全部语言）
        url = 'https://api.bilibili.com/x/player/v2?bvid=%s&cid=%s'%(aid,cid)
        jieshou = requests.get(url,headers=self.headers)
        bvid_dict=my_bvid_dict
        srt_dict = jieshou.json()
        yz = srt_dict['data']['subtitle']['subtitles']      #字幕信息列表
        ming = aid
        i = 0               #计数器
        ii = len(yz)        #字幕语言数量
        if ii == 0:print('【警告】P%s无字幕！'%p)
        while i<ii:                        #循环下载、处理多个语言
            lan = yz[i]['lan']                              #获取字幕的语言编号（ZH JP EN之类）
            suburl = 'http:'+yz[i]['subtitle_url']                  #获取字幕的URL
            mingl = ming + '_P' + str(p) +'_' + lan         #根据视频名、P数和语言生成字幕文件名
            urllib.request.urlretrieve(suburl,'%s.json'%mingl)  #下载json
            self.__jsonZhuanSrt(mingl,bvid_dict['data'][i]['part'])                                 #处理json输出srt
            i += 1
            print ('P%s 第%s种语言下载完成，进度：%s/%s'%(p,i,i,ii))    #报告任务进度（以该P视频的字幕语言数算）
            time.sleep(0.2)


    def __pn(self,bvid):#获取视频列表json
        params = {'bvid':bvid}
        response = self.session.get(self.pagelist_url,headers=self.headers, params=params)
        response_json=response.json()
        bvid_dict=response_json
        #zidian= json.loads(jieshou.text)['data']                   #载入字典
        print ('视频目录获取成功！共%sP。\n'%len(bvid_dict['data']))             #汇报
        return bvid_dict            #返回列表
	
    def __jsonZhuanSrt(self,ming,bvid_name):
        #判断是否经过压缩
        try:
            wenjian = open('%s.json'%ming,encoding='utf-8')
            res=wenjian.read()
        except:
            wenjian = open('%s.json'%ming,'rb')
            data=wenjian.read()
            buff = BytesIO(data)
            f = gzip.GzipFile(fileobj=buff)
            res = f.read().decode('utf-8')
                

        zidian = json.loads(res)['body']            #Json传入字典
        try:
            wenjian.close()
            f.close()
        except:
            pass
        os.remove('%s.json'%ming)
        my_path=self.save_path+'/'+'%s.srt'%bvid_name
        wenjian = open(my_path,'w',encoding='utf-8') #创建srt字幕文件
        i = 0                                   #计数变量
        while i<len(zidian):                    #循环处理每一条字幕
            f = round(zidian[i]['from'],3)      #开始时间 （round(n，3)四舍五入为三位小数）
            t = round(zidian[i]['to'],3)        #结束时间
            c = zidian[i]['content']            #字幕
            ff = time.strftime("%H:%M:%S",time.gmtime(f)) + ',' + self.__miao(f)   #秒数转 时:分:秒 格式，加逗号和毫秒
            tt = time.strftime("%H:%M:%S",time.gmtime(t)) + ',' + self.__miao(t)   #结束时间，处理方式同上
            shujv = str(i+1)+'\n' + ff+' '+'-->'+' '+tt+'\n' + c+'\n\n'     #格式化为Srt字幕
            wenjian.write(shujv)                                            #写入
            i += 1                                                          #计数器+1
        print ('%s OK.'%bvid_name)
	
    def __miao(self,miao):                       #修正毫秒为三位
        miao = str(miao).partition('.')[2]    #取小数部分
        miao+='0'*(3-len(miao))
        return miao                           #返回标准三位的毫秒数
        
    @staticmethod
    def login(username, password):
        _, session = login.Login().bilibili(username, password)
        return session


    def pullFold(self):
        up_mid=input('输入自己的up号:  ')
        #输错会导致拉取的是400
        try:
            bili_folder=self.getFolderIfno(up_mid)
            fold_list=range(0,len(bili_folder['fold_name']))
            for i in fold_list:
                 print("{0}.{1}".format(i,bili_folder['fold_name'][i]))
            folder_num=int(input("选择要下载的收藏夹:"))
            assert (folder_num in fold_list),"选择超出范围"
            self.__setSavePath(r'./'+bili_folder['fold_name'][folder_num])
             #调用实际下载函数
            self.__downFolder(bili_folder['fold_name'][folder_num],bili_folder['fold_id'][folder_num],bili_folder['media_count'][folder_num])
        except:
            print("up号错误")
            os._exit(1)

    def getFolderIfno(self,up_mid:str)->dict:
        params = {'up_mid':up_mid}
        response = self.session.get(self.fold_url, headers=self.headers, params=params)
        response_json = response.json()
        bili_folder={'fold_name':[],'fold_id':[],'media_count':[]}
        for i in response_json['data']['list']:
            bili_folder['fold_name'].append(i['title'])
            bili_folder['fold_id'].append(i['id'])
            bili_folder['media_count'].append(i['media_count'])
        #发布
        return bili_folder
    
    def __getLocalVideoInfo(self):
        time_list=[]
        if os.path.exists('videoinfo.txt'):
            p=open('./videoinfo.txt','r')
            VideoInfo=p.readlines()
            #清除换行符
            for i in range(0,len(VideoInfo)):
                VideoInfo[i]=VideoInfo[i][: -1]
            p.close()
            return VideoInfo
            #print(str(time_list[0])+"  "+str(time_list[1]))
        else:
        #print('no ok')
            return []
        
       
        return time_list
    def downloadVideo(self,bvid):
        self.__downloadVideo(bvid)

    def __downFolder(self,fold_title,fold_id,video_count):
        bvid_queue=[]
        #获取收藏夹内的视频情况
        downed_video=self.__getLocalVideoInfo()
        params = {'media_id': fold_id,'pn':1,'ps':20,'keyword':'','order':'mtime','type':0,'tid':0,'platform':'web','jsonp':'jsonp'}
        while len(bvid_queue)<video_count:
            response = self.session.get(self.foldlist_url, headers=self.headers, params=params)
            response_json=response.json()
            down_queue=response_json['data']['medias']
            for i in down_queue:
                bvid_queue.append(i['bvid'])
            params['pn']+=1
            time.sleep(3)
        #去除已经下载的视频
        bvid_queue=self.__pickDuplicate(bvid_queue,downed_video)
        #遍历下载
        f=open('./videoinfo.txt','a',encoding='utf-8')
        for i in bvid_queue:
            self.__downloadVideo(i)
            if not (i in downed_video):
                f.write(str(i)+'\n')
            try:
                self.getVideoSrt(i)
            except:
                print("{} 字幕下载失败 ".format(i))
        f.close()

        
    def __pickDuplicate(self,bvid_queue,downed_video):
        for i in downed_video:
            if i in bvid_queue:
                bvid_queue.remove(i)
        if (len(bvid_queue)==0):
            print("无需下载")
            sys.exit(0)
        return bvid_queue





'''run'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='下载B站指定用户的所有视频(仅支持Windows下使用)')
    #parser.add_argument('--username', dest='username', help='用户名', type=str, required=True)
    #parser.add_argument('--password', dest='password', help='密码', type=str, required=True)
    #args = parser.parse_args()
    username='账号'
    password='密码'
    bili = Bilibili(username,password)
    choice=input("1.下载up主空间全部\n2.收藏夹\n")
    if(choice=='1'):
        bili.run()
    else:
        while True:
            bili.pullFold()
#李弦月 83335824
#黑大帅的潇洒哥 294675228

#球球很困 414957737
#月柒 353611015