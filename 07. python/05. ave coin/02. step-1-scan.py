import requests
import ast
import sqlite3
import time

def coins():
	url = "https://api.opencc.xyz/v1api/v2/pairs?pageNO=1&pageSize=50&sort=created_at&direction=desc&chain=bsc&minPoolSize=50000"
	headers = {
		"User-Agent": "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B176 Safari/7534.48.3",
		"X-Auth" : "d124c6e4997736c6693f35e106c267c11652723073654281633"
			}
	a = requests.get(url=url,headers=headers).json()
	test = a['data']
	data_coin_dict = ast.literal_eval(test)
	data_coin = data_coin_dict['data']

	return data_coin

def db_create():
	conn = sqlite3.connect('test.db')
	print ("数据库打开成功")
	c = conn.cursor()
	c.execute('''
		CREATE TABLE ave_coin
	       (ID INT PRIMARY KEY,
	       Contract        TEXT    NOT NULL,
	       Pair            TEXT     NOT NULL,
	       CreateTime      TEXT     NOT NULL
	       );
	       ''')
	print ("数据表创建成功")
	conn.commit()
	conn.close()

def db_inert(ID,Contract,Pair,CreateTime):
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	print ("数据库打开成功")
	sql = "INSERT INTO ave_coin (ID,Contract,Pair,CreateTime) VALUES ({}, '{}','{}','{}' )".format(ID,Contract,Pair,CreateTime)
	c.execute(sql)
	conn.commit()
	print ("数据插入成功")
	conn.close()

def main():
	ave_coins = coins()
	ID = 0
	for i in ave_coins:
		ID += 1

		Contract = i['target_token']
		Pair = i['token0_symbol'] +"/"+i['token1_symbol']

		CreateTime = i['created_at']
		CreateTime = time.localtime(CreateTime)
		CreateTime = time.strftime("%Y-%m-%d", CreateTime)
		print("序号: {}  合约: {}   币名: {}    创建时间: {}".format(ID,Contract,Pair,CreateTime))

		db_inert(ID,Contract,Pair,CreateTime)

if __name__ == '__main__':
	db_create()
	main()
