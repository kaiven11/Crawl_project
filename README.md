1.爬取关键字为“风景”的相关文章，包括链接、标题、公众号、文章内容等相关信息，并保存在名为items.jl的文件中。
  链接地址为：http://weixin.sogou.com， 因持续从微信爬去文章，触发其反代理机制。为避免此情况，在下载中间件中根据返回的情况进行更换代理。
  代理可从我的源找到下载并运行。
 

2.爬取安居客关键字的所有房源信息，并记录到excel表中。

  https://bj.zu.anjuke.com/?kw=%E8%A7%92%E9%97%A8%E4%B8%9C%E9%87%8C%E5%B0%8F%E5%8C%BA&k_comm_id=848519&cw=%E8%A7%92%E9%97%A8%E4%B8%9C%E9%87%8C%E5%B0%8F%E5%8C%BA

3.爬去煎蛋中的妹子图片，并基于scrapyd发布部署到云ECS服务器上。
  http://jandan.net/ooxx
  
  爬取图片这里就没有必要细说了，主要说下我是如何来部署的。
  
  环境：windows 10 + 阿里云 ECS服务器（ubuntu系统）
  一.服务器配置：
    
    pip3 install scrapyd
    pip3 install nginx
    
    因为scrapyd默认是在本机的6800端口打开，只能本机访问，这里用nginx做了一个代理，在/etc/nginx/site-enabled/ 目录下,
    新建一个scrapyd.conf 文件，并添加如下的配置文件内容：
     server {
            listen 6801;
            location / {
                    proxy_pass            http://127.0.0.1:6800/;
                    auth_basic            "Restricted";
                    auth_basic_user_file  /etc/nginx/conf.d/.htpasswd;
            }
      }
    
     
     生成认证文件：
     在上面配置的 auth_basic_user_file 中　生成密码文件，运行 htpasswd -c .htpasswd xxxxx,接着输入密码即可创建完成
     （apt install apache2-utils #如果系统没有htpasswd，运行此命令进行安装）
     启动服务：
        运行   nohup scrapyd &
        此时重启nginx服务，并运行   service nginx start
     
     最后一步是在阿里云的控制台打开入方向的6800端口，否则仍旧是不能访问。
    
 二.客户端配置
    
    pip3 install scrapyd-client
    
    在 C:\Python35\Scripts 下新建两个文件：scrapy.bat scrapyd-deploy.bat
    在scrapy中写入如下内容：
     
    @echo off
    c:\Python35\python c:\Python35\Scripts\scrapy %*
     
    在scrapyd-deploy.bat中写入下面内容：
    
    @echo off
    c:\Python35\python c:\Python35\Scripts\scrapyd-deploy %*
    
    此时可在浏览器直接运行scrapyd-deploy命令
    
    此时客户端配置完成
    
 三.部署服务
    
    1.修改爬虫项目里的scrapy.cfg,
    [deploy]
    url = http://xx.xx.xx.xx:6801/
    project = jiandan
    username = xxxx
    password = xxxxx
    
    2.打开cmd命令，进入项目根目录
      运行scrapyd-deploy(打包项目并部署)
    3.部署完成后，启动爬虫计划
      curl http://xx.xx.xx.xx:6801/schedule.json -d project=jiandan -d spider=jiandanspider -u username:password #前面设置的用户名和密码
      运行后，会有返回提示，成功为success ，同时包括jobid
    4.停止一个任务
      curl http://xx.xx.xx.xx:6801/cancel.json -d project=jiandan -d job= 8270364f9d9811e5adbf000c29a5d5be #上面的jobID
    
    以上就是部署爬虫项目的完整配置。
    
     
     
