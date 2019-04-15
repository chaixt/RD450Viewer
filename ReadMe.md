# 针对ThinkServer RD450所使用的管理程序

##依赖项
 - jre 6+
 - python 2.7
 - urllib 0.1.12+
 - pycurl 7.19.5.3+
 - certifi 2017.7.27.1+
 
 
## 使用方式
${Server}有ThinkServerRD450/DellR430/IBMx3650M5
```
python ${Server}.py 主机名 用户名 密码 [代理ip 代理端口]
```
 - 主机名为服务器管理端口ip
 - 用户名密码为管理端WEB的登陆用户名密码
 - 代理采用socks4/5，可使用ssh隧道
 
 
## 注意
只考虑Windows。Java虚拟机需要与系统一致，根据系统的位数加载动态库
