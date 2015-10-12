
import time
import json
import os
import subprocess

def m1():
	#MAIN PROCESSSING
	t = open("attackURLnFile.txt",'w')
	t.close()
	
	temp_file = open("input.json",'r')
	data = json.load(temp_file)
	data2 = data[0]
	index=0
	
	'''
	initfiles = ["attackURLnFile.txt", "step3op.json", "step3loginop.json", "data.json", "datalogin.json", "Singleinput.json"]
	for tf in initfiles:
		t = open(tf,'w');
		if tf != "attackURLnFile.txt":
			t.write("[]")
		t.close()
	'''
			
	# call scanner for all values in the input file
	count = 0
	for key,value in data2.iteritems():
		count +=1
		#print count
		abc = []
		'''
		print "KEY: " + key
		print "VALUE: " + str(value)
		print "LENGTH: " + str(len(value))
		print "TYPE: " + str(type(value))
		'''
		for val in value:
			#print "VAL: " + str(val)
	
			if ((val["params"][0]["username"] is None or val["params"][0]["username"] == "")
				or (val["params"][0]["password"] is None or val["params"][0]["password"] == "")):
				val["loginRequired"]="false"
			else:
				val["loginRequired"]="true"
			abc = [{key:[val]}]
			f1 = open("Singleinput.json",'w')
			#print abc
			f1.write(json.dumps(abc, indent=4))
			f1.close()
			os.system("sh test.sh")
			print abc 
			'''f1 = open("Singleinput.json",'w')
			a1="[{}]"
			f1.write(a1)'''
			f1.close()
		
		'''
		if ((type(value) is list) & (len(tempValue)>1)):
			index=len(tempValue)
			print "----" + str(tempValue)
			print str(index) + ": " + str(key) + ": " + str(value)
			while (index>0):
				abc=[]
			
				index=index-1
				value1 = [tempValue[index]]
				#print "typ1"
				#print type(value1)
				if ((value1[0].get("params")[0].get("username") is None or value[0].get("params")[0].get("username") == "")
				or (value1[0].get("params")[0].get("password") is None or value[0].get("params")[0].get("password") == "")):
					value1[0]["loginRequired"]="false"
				else:
					value1[0]["loginRequired"]="true"
				abc.append({key:value1})
				f1 = open("Singleinput.json",'w')
				#print abc
				f1.write(json.dumps(abc, indent=4))
				f1.close()
				#os.system("sh test.sh")
				if(index==0):
					break
				#print "next script: "
			
				print "Step1....."
				os.system("scrapy crawl step1 > step1.txt")
				os.system("scrapy crawl step1login > step1login.txt")
				print "Step3....."
				os.system("scrapy crawl step3login > step3login.txt")
				os.system("scrapy crawl step3 > step3.txt")
				#time.sleep(5)
				print "Step4....."
				os.system("python -c 'import step4; print step4.main();'")
			
			
		else:
			print "asdasdad " + str(index) + ": " + str(key) + ": " + str(value)
			#print (value[0])
			if ((value[0].get("params")[0].get("username") is None or value[0].get("params")[0].get("username") == "")
				or (value[0].get("params")[0].get("password") is None or value[0].get("params")[0].get("password") == "")):
					value[0]["loginRequired"]="false"
			else:
					value[0]["loginRequired"]="true"
			abc.append({key:value})
			f1 = open("Singleinput.json",'w')
			#print abc
			f1.write(json.dumps(abc, indent=4))
			f1.close()
			#os.system("sh test.sh")
			#print "next script: " 
		
			print "Step1....."
			os.system("scrapy crawl step1 > step1.txt")
			os.system("scrapy crawl step1login > step1login.txt")
			print "Step3....."
			os.system("scrapy crawl step3login > step3login.txt")
			os.system("scrapy crawl step3 > step3.txt")
			print "Step4....."
			os.system("python -c 'import step4; print step4.main();'")
		
	#os.system("python -c 'import step4; print step4.main();'")
	#subprocess.Popen(["scrapy","crawl","step1"])
	#subprocess.Popen(["scrapy","crawl","step1login"])
	#subprocess.Popen(["scrapy","crawl","step3","-s","LOG_ENABLED=0"])
	#subprocess.Popen(["python -c 'import step4; print step4.main();'"])
	'''
