# 针对ThinkServer RD450所使用的管理程序

##依赖项
 - jre 6+
 - python 2.7
 - urllib 0.1.12+
 - pycurl 7.19.5.3+
 - certifi 2017.7.27.1+
 
 
## 使用方式
```
python pyviewer.py 主机名 用户名 密码 [代理ip 代理端口]
```
 - 主机名为服务器管理端口ip
 - 用户名密码为管理端WEB的登陆用户名密码
 - 代理采用socks4/5，可使用ssh隧道
 
 
## 注意
该程序默认为Win64，如需要Win32，将Win32.jar解压替换dll
