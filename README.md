# one program for helping input the console with gui
一个带gui的自动填写的工具，通过txt编写好提前的配置脚本

for example(例子)
xxx.txt

cd /home
ls -l

meaning:

shell
`cd /home`
`ls -l`


xxx.txt

cd /home#
ls -l

shell:
`cd /home`#waiting somettimes (oringin 10 s)
`ls -l`



# bug.py和bug.exe是用来爬取起点更新的，就是爬取作品的最新章节，主要用处就是看作家有没有更新
然后应当在同一目录下建立一个名为url.txt的文本文件，每一行都是一个起点作品首页
作用:就是快速检查起点作家是否有更新,

quick_input是针对不能复制黏贴的情况下，快速模拟键盘输入英文命令


# b站测试是b站爬虫
功能:<br>
>1.可以根据up主的id号来爬取空间的所有视频<br>
>2.爬取自己的收藏夹,增量下载收藏夹下的视频<br>
  
配置:<br>
>必须配置自己的账号密码在main函数内,原版是通过命令行的方式输入的,但由于是个人私用的代码,我就改成了硬编码账号和密码的方式,自己用起来方便就完事<br>
>写gui没啥必要,自己用的,能少写几十行代码呢.<br>


个人努力:<br>
>1.规范化了部分代码,将单个视频下载,视频信息获取功能和字幕文件下载功能单独抽离成可被对外调用的函数<br>
>2.根据网上资料,增加了增量爬取自己收藏夹视频的功能<br>

代码来源:<br>
>视频下载代码参考了<br> 
>charles的皮卡丘 公众号的b站下载代码,和用了他的登录库.<br>
>字幕下载部分来自:<br>
>https://tieba.baidu.com/p/6222744697<br>










