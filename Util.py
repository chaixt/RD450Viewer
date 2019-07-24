#coding=utf-8
'''
Created on 2019-04-14
@author: ²ñÏòÍ£
@description: RD450Ô¶³ÌµÇÂ½³ÌĞò
ÒÀÀµ¿â(·ÇÏµÍ³¿â)£º
		urllib (0.1.12)
		pycurl (7.19.5.3)
'''

import urllib;
import pycurl;
import StringIO;
import certifi;
import platform;

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
def HttpOperDebug(debug_type, debug_msg):
	print "debug(%d): %s" % (debug_type, debug_msg)


class HttpOper:
	def __init__(self, isDebug=False):
		self.headers = "";
		self.curl = pycurl.Curl();
		self.curl.setopt(pycurl.CAINFO, certifi.where())
		self.curl.setopt(pycurl.SSL_VERIFYPEER, False);
		self.curl.setopt(pycurl.SSL_VERIFYHOST, False);
		self.bodyio = StringIO.StringIO();
		self.headerio = StringIO.StringIO();
		self.curl.setopt(pycurl.WRITEFUNCTION, self.bodyio.write);
		self.curl.setopt(pycurl.HEADERFUNCTION, self.headerio.write);
		self.curl.setopt(pycurl.COOKIEFILE,"");
		self.curl.setopt(pycurl.CONNECTTIMEOUT, 60);
		self.curl.setopt(pycurl.TIMEOUT, 120);
		if isDebug:
			self.curl.setopt(pycurl.VERBOSE, 1)
			self.curl.setopt(pycurl.DEBUGFUNCTION, HttpOperDebug);
		self.isDump = False;

	def __del__(self):
		pass

	def setProxy(self, proxy, up=None):
		self.curl.setopt(pycurl.PROXYTYPE, 5)
		self.curl.setopt(pycurl.PROXY, proxy)
		if(up != None):
			self.curl.setopt(pycurl.PROXYUSERPWD, up)
			
	def setCookie(self, cookieMap):
		self.curl.setopt(pycurl.COOKIE, cookieMap if type(cookieMap) == str else ";".join(Map2UrlList(cookieMap)));
		
	def setHeaders(self, headers):
		self.curl.setopt(pycurl.HTTPHEADER, headers);
		
	def setReferer(self, url):
		self.curl.setopt(pycurl.REFERER, url);
		
	def Request(self):
		self.curl.perform();
		rslt = self.bodyio.getvalue();
		self.headers = self.headerio.getvalue();
		self.headerio.truncate(0);
		self.bodyio.truncate(0);
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
	def GetCode(self):
		return self.curl.getinfo(pycurl.HTTP_CODE)
		
	def GetCookies(self):
		rcs=[];
		cookies = self.curl.getinfo(pycurl.INFO_COOKIELIST);
		if cookies != None and type(cookies) == list:
			for c in cookies:
				xc = c.split("\t");
				rcs.append("%s=%s" % (xc[5], xc[6]));
		return rcs;
		
	def GetCookie(self):
		return self.curl.getinfo(pycurl.INFO_COOKIELIST);
				
	def GetRespHeaders(self):
		return self.headers;
		



def getMachine():
	return platform.machine()[-2:];
		
def findmid(s, b, e):
	r=None;
	ibegin=s.find(b);
	if(ibegin >= 0):
		ibegin=ibegin + len(b);
		iend=s.find(e, ibegin);
		if(iend >= 0):
			r = s[ibegin:iend];
	return r;
	
def findleft(s, b):
	r=None;
	ibegin=s.find(b);
	if(ibegin >= 0):
		ibegin=ibegin + len(b);
		r = s[ibegin:];
	return r;
	