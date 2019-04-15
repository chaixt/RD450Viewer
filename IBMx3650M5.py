#coding=utf-8
'''
Created on 2019-04-15
@author: 柴向停
@description: X3650远程登陆程序
依赖库(非系统库)：
		urllib (0.1.12)
		pycurl (7.19.5.3)
'''

import os;
import sys;
import urllib;
import time;
import getpass;
import json;
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

userinfo = {
	'user': user,
	'password': pwd
};

def buildRequest():
	r = HttpOper();
	if hasProxy:
		r.setProxy("%s:%d"%(phost, pport));
	return r;

def runClass(mc, jparams):
	x=getMachine();
	dlls="Win%s"%x;#这里只考虑Windows，java虚拟机需要与系统一致
	if hasProxy:
		os.system("cd ibm && java -DproxySet=true -DsocksProxyHost=%s -DsocksProxyPort=%d -Djava.library.path=%s -cp avctIBMViewer__V082817.jar %s %s"%(phost, pport, dlls, mc, jparams));
	else:
		os.system("cd ibm && java -Djava.library.path=%s -cp avctIBMViewer__V082817.jar %s %s"%(dlls, mc, jparams));

if __name__ == '__main__':
	m = buildRequest();
	m.setReferer("https://%s/designs/imm/index.php"%host)
	cinfo=m.PostUrl('https://%s/data/login'%host, userinfo);
	cinfo=json.loads(cinfo);
	cookies=m.GetCookie();
	st=cinfo["status"];
	ar=cinfo["authResult"];
	tkn=cinfo["token1_name"];
	tkv=cinfo["token1_value"];
	if st == "ok" and ar == "0" and tkn != None and tkv != None:
		tt="443";
		m.setCookie(";".join(cookies));
		jnlp=m.GetUrl("https://%s/designs/imm/viewer(%s@%s@0@%d@1@1@0@jnlp@%s@0@0@0@0@1).jnlp?%s=%s"%(host, host, tt, (time.time()*1000), user, tkn, tkv));
		jparams=findmid(jnlp,"<application-desc", "</application-desc>");
		mc = findmid(jparams, " main-class=\"", "\">");
		jparams=findleft(jparams, "\">")
		jparams=jparams.replace("<argument>", "").replace("</argument>", " ").replace("\n", "");
		runClass(mc, jparams);
	else:
		print "Login Fail!"