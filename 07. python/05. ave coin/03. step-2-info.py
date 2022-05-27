import requests
import sqlite3
import ast
import base64
from urllib.parse import urlparse
import time

def hunter(domain):
	key = "ecfbffe0ab717143186a43bd487579b8962e8eb292d0319a92207434a49e3758"
	search = domain
	search = base64.urlsafe_b64encode(search.encode("utf-8"))
	search = search.decode('utf-8')

	url = "https://hunter.qianxin.com/openApi/search?api-key={}&search={}&page=1&page_size=20&is_web=1&status_code=200".format(key,search)
	print("Hunter api:    "+url)
	reps = requests.get(url=url).json()
	arr = reps['data']['arr']

	countrylist = []
	portlist    = []
	cpanellist  = []

	if arr != None:
		for i in arr:
			country = i['country']
			port    = i['port']
			component = i['component']

			countrylist.append(country)
			portlist.append(port)

			if component != None:
				for i in component:
					cpanel = i['name']
					cpanellist.append(cpanel)
	else:
		return ["","","","hunter查询无信息"]

	new_countrylist = []
	[	new_countrylist.append(i) for i in countrylist if i not in new_countrylist	]
	new_portlist = []
	[	new_portlist.append(i) for i in portlist if i not in new_portlist	]
	new_cpanellist = []
	[	new_cpanellist.append(i) for i in cpanellist if i not in new_cpanellist	]

	countrystr = ",".join(new_countrylist)
	portstr =",".join('%s' %id for id in new_portlist)
	cpanelstr  = ",".join(new_cpanellist)

	print("域名: {} 端口: {} 国家: {} 指纹: {}".format(domain,portstr,countrystr,cpanelstr))

	if "cPanel" in cpanellist or "Cloudflare" in cpanellist or "2096" in portlist or "2095" in portlist :
		print("pass")
		return ["","","","cdn or Cloudflare or cpanel"]

	elif "BaoTa 宝塔面板 Interface Prompt" in cpanellist:
		cpanelstr = "BaoTa 宝塔面板"
		return [countrystr,portstr,cpanelstr,"宝塔面板"]
	elif "中国" in countrylist or  "美国" in countrylist or  "新加坡" in countrylist:
		return [countrystr,portstr,cpanelstr,"国家符合要求"]
	else:
		return [" "," "," ","待确认"]


def ave_info(data):
	ID 	 = data[0]
	Contract = data[1]
	Pair = data[2]
	CreateTime = data[3]

	url = "https://api.opencc.xyz/v1api/v2/tokens/{}-bsc".format(Contract)
	headers = {
	"User-Agent": "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B176 Safari/7534.48.3",
	"X-Auth" : "d124c6e4997736c6693f35e106c267c11652723073654281633"
		}
	reps = requests.get(url=url,headers=headers).json()
	reps = ast.literal_eval(reps['data'])['token']
	#print(reps)

	#判断是否存在info信息
	if 'appendix' in reps.keys():
		reps = ast.literal_eval(reps['appendix'])
		website = reps['website']

		#info 信息种是否存在 Website
		if website !=  "":
			print("url: "+ website)
			#网站是否带 "/"
			if "/" in website:
				result = urlparse(website)
				result = result.netloc.split('.')
				domain = result[-2]+"."+result[-1]
				print("域名:  "+ domain)
				time.sleep(1.5)
				hunter_data = hunter(domain)
				Country = hunter_data[0]
				Port    = hunter_data[1]
				Finger  = hunter_data[2]
				Remarks = hunter_data[3]
				db_inert_ave_coin_info_hunter(Contract,Pair,CreateTime,website,Country,Port,Finger,Remarks)
				
			else:
				domain = website
				print("域名:  "+ domain)
				time.sleep(1.5)
				hunter_data = hunter(domain)
				Country = hunter_data[0]
				Port    = hunter_data[1]
				Finger  = hunter_data[2]
				Remarks = hunter_data[3]
				db_inert_ave_coin_info_hunter(Contract,Pair,CreateTime,website,Country,Port,Finger,Remarks)
		else:
			Website = ''
			Twitter = ''
			db_inert_ave_coin_info_null(Contract,Pair,CreateTime,Website,Twitter)
	else:
		Website = ''
		Twitter = ''
		db_inert_ave_coin_info_null(Contract,Pair,CreateTime,Website,Twitter)

def db_create():
	conn = sqlite3.connect('test.db')
	print ("数据库打开成功")
	c = conn.cursor()
	c.execute('''
		CREATE TABLE ave_coin_info_null
	       (ID INTEGER PRIMARY KEY,
	       Contract        TEXT    NOT NULL,
	       Pair            TEXT     NOT NULL,
	       CreateTime      TEXT     NOT NULL,
	       Website      TEXT     ,
	       Twitter      TEXT     
	       );
	       ''')

	c.execute('''
		CREATE TABLE ave_coin_info_hunter
	       (ID INTEGER PRIMARY KEY,
	       Contract        TEXT    NOT NULL,
	       Pair            TEXT     NOT NULL,
	       CreateTime      TEXT     NOT NULL,
	       Website         TEXT     ,
	       Country         TEXT     ,
	       Port      	   TEXT     ,
	       Finger    	   TEXT     ,
	       Remarks		   TEXT
	       );
	       ''')
	print ("数据表创建成功")
	conn.commit()
	conn.close()


def db_inert_ave_coin_info_null(Contract,Pair,CreateTime,Website,Twitter):
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	print ("数据库打开成功")
	sql = "INSERT INTO ave_coin_info_null (Contract,Pair,CreateTime,Website,Twitter) VALUES ('{}','{}','{}' ,'{}','{}')".format(Contract,Pair,CreateTime,Website,Twitter)
	c.execute(sql)
	conn.commit()
	print ("数据插入成功")
	conn.close()

def db_inert_ave_coin_info_hunter(Contract,Pair,CreateTime,Website,Country,Port,Finger,Remarks):
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	sql = "INSERT INTO ave_coin_info_hunter (Contract,Pair,CreateTime,Website,Country,Port,Finger,Remarks) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}' )".format(Contract,Pair,CreateTime,Website,Country,Port,Finger,Remarks)
	c.execute(sql)
	conn.commit()
	print ("数据插入成功")
	conn.close()


def data_db():
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	datas = []
	sql = "SELECT ID,Contract,Pair,CreateTime  from  ave_coin where id > 1032 "
	cursor = c.execute(sql)
	for row in cursor:
		temp = []
		temp.append(row[0]);temp.append(row[1]);temp.append(row[2]);temp.append(row[3]);
		datas.append(temp)

	#print(data)
	print ("数据操作成功")
	conn.close()

	return datas

def main():
	datas = data_db()
	for data in datas:
		try:
			ave_info(data)
		except:
			print('[-]连接异常!')



if __name__ == '__main__':
	#db_create()
	main()



