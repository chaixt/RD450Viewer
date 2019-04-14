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
import pycurl;
import StringIO;
import collections;
import certifi;

def Map2UrlList(amap):
	rtList = [];
	for key in amap.keys():
		val = amap[key];
		if isinstance(val, (str, unicode)):
			rtList.append("=".join([key, urllib.quote(val)]));
		else:
			if(len(val) >= 1):
				for v in val:
					rtList.append("=".join([key, urllib.quote(v)]));
	return rtList;

def Dump2File(filename, str):
	output = open(filename, "w");
	output.write(str);
	output.close();


__version__ = "0.1";


class HttpRequest:
	def __init__(self):
		self.curl = pycurl.Curl();
		self.curl.setopt(pycurl.CAINFO, certifi.where())
		self.curl.setopt(pycurl.SSL_VERIFYPEER, False);
		self.curl.setopt(pycurl.SSL_VERIFYHOST, False);
		self.strio = StringIO.StringIO();
		self.curl.setopt(pycurl.WRITEFUNCTION, self.strio.write);
		self.curl.setopt(pycurl.COOKIEFILE,"");
		self.curl.setopt(pycurl.CONNECTTIMEOUT, 60);
		self.curl.setopt(pycurl.TIMEOUT, 120);
		self.isDump = False;

	def __del__(self):
		pass

	def setProxy(self, proxy, up=None):
		self.curl.setopt(pycurl.PROXYTYPE, 5)
		self.curl.setopt(pycurl.PROXY, proxy)
		if(up != None):
			self.curl.setopt(pycurl.PROXYUSERPWD, up)
			
	def setCookie(self, cookieMap):
		self.curl.setopt(pycurl.COOKIE, ";".join(Map2UrlList(cookieMap)));
		
	def Request(self):
		self.curl.perform();
		rslt = self.strio.getvalue();
		self.strio.truncate(0);
		return rslt;

	def setDump(self, isDump):
		self.isDump = isDump;

	def dump(self, fn, content):
		if self.isDump:
			Dump2File(fn, content);

	def GetUrl(self, url, dataMap=None):
		if dataMap != None:
			self.curl.setopt(pycurl.URL, "/".join([url, "&".join(Map2UrlList(dataMap))]));
		else:
			self.curl.setopt(pycurl.URL, url);
		return self.Request();

	def PostUrl(self, url, dataMap={}):
		self.curl.setopt(pycurl.URL, url);
		self.curl.setopt(pycurl.POSTFIELDS, "&".join(Map2UrlList(dataMap)));
		return self.Request();

hasProxy=False;
phost="127.0.0.1";
pport=1080;
host="127.0.0.1"
user="root"
pwd="root"

if(len(sys.argv) < 4):
	print "%s host user password [proxyhost proxyport]"%sys.argv[0]
	exit();
	
host=sys.argv[1];
user=sys.argv[2];
pwd=sys.argv[3];
if len(sys.argv) > 4:
	hasProxy=True;
	phost=sys.argv[4];
	if len(sys.argv) > 5:
		pport=sys.argv[5];


userinfo = {
	"WEBVAR_USERNAME":user,
	"WEBVAR_PASSWORD":pwd
};

def buildRequest():
	r = HttpRequest();
	if hasProxy:
		r.setProxy("%s:%d"%(phost, pport));
	return r;
def runJar(jar, jparams):
	if hasProxy:
		os.system("cd lib && java -DproxySet=true -DsocksProxyHost=%s -DsocksProxyPort=%d -jar %s %s"%(phost, pport, jar, jparams));
	else:
		os.system("cd lib && java -jar %s %s"%(jar, jparams));
def findmid(s, b, e):
	r=None;
	ibegin=s.find(b);
	if(ibegin >= 0):
		ibegin=ibegin + len(b);
		iend=s.find(e, ibegin);
		if(iend >= 0):
			r = s[ibegin:iend];
	return r;

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
		runJar("JViewer.jar", jparams);
	else:
		print "Login Fail!"