import requests
import urllib3
import sqlite3
from queue import Queue
import threading
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class cdnScan(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue
    def run(self):
        while not self._queue.empty():
            i = self._queue.get()
            getTargets(i)

            '''
            try:
            	getTargets(i)
            except:
                print('[-]连接异常!')
            '''
            
#使用https://www.coingecko.com 查看代币名称和代币详细信息的href。
#['Total Crypto Market Cap','/en/coins/piedao-dough-v2']
def name(num):
	url = 'https://www.coingecko.com/?page='+str(num)

	header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
	res = requests.get(url,verify=False,headers=header)
	soup = BeautifulSoup(res.text,'lxml')
	result = soup.find_all(name='a',class_='tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between')

	results = []
	for a in result:
		# 获取项目名字
		temp = []
		soup = BeautifulSoup(str(a),'lxml')
		name = soup.a.text
		name = name.replace('\n', '')
		temp.append(name)

		# 获取A标签中的href
		#	for a in soup.findAll('a',href=True):
	    #	print a['href']
		href_tags = [ tag['href'] for tag in soup.findAll('a',{'href':True}) ]
		href_tags_url = href_tags[0]

		temp.append(href_tags_url)

		results.append(temp)
	return results

#使用https://www.coingecko.com 查看代币的官方网站。
def website(results):
	#	results[0] 为代币名称     results[1] 代币项目信息的href
	url = results[1]
	url = "https://www.coingecko.com"+str(url)

	header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
	res = requests.get(url,verify=False,headers=header)
	soup = BeautifulSoup(res.text,'lxml')
	result = soup.find_all(name='div',class_='tw-flex flex-wrap tw-font-normal')

	Websile_soup = result[0]
	soup = BeautifulSoup(str(Websile_soup),'lxml')
	result = soup.find_all(name='a',class_='tw-px-2.5 tw-py-1 tw-my-0.5 tw-mr-1 tw-rounded-md tw-text-sm tw-font-medium tw-bg-gray-100 tw-text-gray-800 hover:tw-bg-gray-200 dark:tw-text-white dark:tw-bg-white dark:tw-bg-opacity-10 dark:hover:tw-bg-opacity-20 dark:focus:tw-bg-opacity-20')

	result2 = []
	result2.append(results[0])

	Websile = []
	for a in result:
		soup = BeautifulSoup(str(a),'lxml')
		name = soup.a.text
		Websile.append(name)

	result2.append(Websile)
	return result2

def getTargets(num):
	results = name(num)
	for i in results:
		a = website(i)
		print(a)

		CoinName = a[0]
		CoinWeb  = a[1]

		# 代币存入数据库中
		conn = sqlite3.connect('coin.db')

		sql = "INSERT INTO CoinAll (coin) VALUES  (\""+str(CoinName)+"\") "
		c = conn.cursor()    #print ("数据库打开成功")
		c.execute(sql)

		# 查询Coin所属id值
		# SELECT id from CoinAll WHERE coin = ''
		sql = "SELECT id from CoinAll where coin =\""+CoinName+"\" "
		cursor = c.execute(sql)
		coinid = [row[0] for row in cursor]
		
		uid = coinid[0]
		# 将Website插入
		for web in CoinWeb:
			sql = "INSERT INTO CoinWeb (Coin_id,coin,website) VALUES  ('{}','{}','{}') ".format(str(uid),str(CoinName),str(web))
			c.execute(sql)
		conn.commit()
		conn.close()




def main():
	# 获取50页到137页的数据
    queue = Queue()
    for i in range(50,137):
        print("第{}页数据正在提取...".format(i))
        queue.put(i)

    threads = []
    thread_count = 10
    for i in range(thread_count):
        threads.append(cdnScan(queue))
    for t in threads:
        t.start()
    for t in threads:
        t.join()




if __name__ == '__main__':
	main()
	




