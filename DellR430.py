#coding=utf-8
'''
Created on 2019-04-15
@author: 柴向停
@description: R430远程登陆程序
依赖库(非系统库)：
		urllib (0.1.12)
		pycurl (7.19.5.3)
'''

import os;
import sys;
import urllib;
import time;
import getpass;
import collections;
from Util import HttpOper,findmid,findleft,getMachine;

__version__ = "0.1";


hasProxy=False;
phost="127.0.0.1";
pport=1080;
host="127.0.0.1"
user="root"
pwd="root"

if(len(sys.argv) < 3):
	print "%s host user [proxyhost proxyport]"%sys.argv[0]
	exit();
	
host=sys.argv[1];
user=sys.argv[2];
if len(sys.argv) > 3:
	hasProxy=True;
	phost=sys.argv[3];
	if len(sys.argv) > 4:
		pport=int(sys.argv[4]);

pwd=getpass.getpass("Please input password:");
while pwd == '':
	pwd=getpass.getpass("Password couldn't be Empty! Please input password:");

userinfo = collections.OrderedDict();
userinfo["user"]=user;
userinfo["password"]=pwd;


def buildRequest():
	r = HttpOper();
	if hasProxy:
		r.setProxy("%s:%d"%(phost, pport));
	return r;

def runClass(mc, jparams):
	x=getMachine();
	dlls="Win%s"%x;#这里只考虑Windows，java虚拟机需要与系统一致
	if hasProxy:
		os.system("cd dell && java -DproxySet=true -DsocksProxyHost=%s -DsocksProxyPort=%d -Djava.library.path=%s -cp avctKVM.jar %s %s"%(phost, pport, dlls, mc, jparams));
	else:
		os.system("cd dell && java -Djava.library.path=%s -cp avctKVM.jar %s %s"%(dlls, mc, jparams));

if __name__ == '__main__':
	m = buildRequest();
	cinfo=m.PostUrl('https://%s/data/login'%host, userinfo);
	cookies=m.GetCookie();
	st=findmid(cinfo, "<status>", "</status>");
	ar=findmid(cinfo, "<authResult>", "</authResult>");
	fu=findmid(cinfo, "<forwardUrl>", "</forwardUrl>");
	if st == "ok" and ar == "0" and fu != None:
		tt="PowerEdge";
		str1=findmid(fu, "index.html?", ",ST2=");
		m.setCookie(";".join(cookies));
		jnlp=m.GetUrl("https://%s/viewer.jnlp(%s@0@%s@%d@%s"%(host, host, tt, (time.time()*1000), str1));
		jparams=findmid(jnlp,"<application-desc", "</application-desc>");
		mc = findmid(jparams, " main-class=\"", "\">");
		jparams=findleft(jparams, "\">")
		jparams=jparams.replace("<argument>", "").replace("</argument>", " ").replace("\n", "");
		runClass(mc, jparams);
	else:
		print "Login Fail!"