import requests
import sqlite3
import urllib3
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 代币存入数据库中
conn = sqlite3.connect('coin.db')
c = conn.cursor()    #print ("数据库打开成功")

sql = '''
	SELECT IP from CoinWeb where IP != 'CDN' 
	  '''
cursor = c.execute(sql)
ips = [row[0] for row in cursor]

for ip in ips:
	try:
		url = "https://api.ip138.com/ip/?ip={}&datatype=jsonp&token=0a3f0439a8f45fae49a8c85f8195ede3".format(ip)
		resp = requests.get(url=url,verify=False)

		print(resp.json()['ip'])
		print(resp.json()['data'][0])
		sql = "UPDATE CoinWeb  SET (ascription)  =  ('{}') WHERE ip = '{}'".format(resp.json()['data'][0],resp.json()['ip'])
		print(sql)
		c.execute(sql)
		conn.commit()
		print("Total number of rows updated :", conn.total_changes)
	except:
		print('[-]连接异常!')

conn.close()
