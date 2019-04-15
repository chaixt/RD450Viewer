#coding=utf-8
'''
Created on 2019-04-14
@author: 柴向停
@description: RD450远程登陆程序
依赖库(非系统库)：
		urllib (0.1.12)
		pycurl (7.19.5.3)
'''

import os;
import sys;
import urllib;
import StringIO;
import getpass;
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
	"WEBVAR_USERNAME":user,
	"WEBVAR_PASSWORD":pwd
};



def buildRequest():
	r = HttpOper();
	if hasProxy:
		r.setProxy("%s:%d"%(phost, pport));
	return r;
		
		

def runClass(jparams):
	x=getMachine();
	dlls="Win%s"%x;#这里只考虑Windows，java虚拟机需要与系统一致
	if hasProxy:
		os.system("cd thinkserver && java -DproxySet=true -DsocksProxyHost=%s -DsocksProxyPort=%d -Djava.library.path=%s -jar JViewer.jar %s"%(phost, pport, dlls, jparams));
	else:
		os.system("cd thinkserver && java -Djava.library.path=%s  -jar JViewer.jar %s"%(dlls, jparams));
		
if __name__ == '__main__':
	m = buildRequest();
	cinfo=m.PostUrl('https://%s/rpc/WEBSES/create.asp'%host, userinfo);
	sc=findmid(cinfo, "'SESSION_COOKIE' : '", "'");
	ip=findmid(cinfo, "'BMC_IP_ADDR' : '", "'");
	tk=findmid(cinfo, "'CSRFTOKEN' : '", "'");
	if sc != None and ip != None and tk != None:
		m = buildRequest();
		m.setCookie({
			"SessionCookie":sc,
			"BMC_IP_ADDR":ip,
			"CSRFTOKEN":tk
		});
		jnlp=m.GetUrl("https://%s/Java/jviewer.jnlp?EXTRNIP=%s&JNLPSTR=JViewer"%(host, ip));
		jparams=findmid(jnlp,"<application-desc>", "</application-desc>");
		jparams=jparams.replace("<argument>", "").replace("</argument>", " ").replace("\n", "");
		runClass(jparams);
	else:
		print "Login Fail!"