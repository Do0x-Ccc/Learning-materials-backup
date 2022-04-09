from selenium import webdriver
from bs4 import BeautifulSoup
import time
from queue import Queue
import threading
import sqlite3

class cdnScan(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue
    def run(self):
        while not self._queue.empty():
            host = self._queue.get()
            try:
                options = webdriver.ChromeOptions()
                options.add_argument(
                    'user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--headless')
                options.add_argument('blink-settings=imagesEnabled=false')
                options.add_argument('--disable-gpu')
                driver = webdriver.Chrome(options=options)
                driver.get('https://ping.chinaz.com/{}'.format(host))
                time.sleep(5)
                bf = BeautifulSoup(driver.page_source, 'lxml')
                driver.quit()
                result = bf.find_all('div', class_='Cont')
                result = result[0].find_all('a')

                if len(result) > 1:
                    print('[-]目标({})使用了CDN服务！\n'.format(host))
                    '''
                    # 插入数据库
                    '''
                    conn = sqlite3.connect('coin.db')
                    c = conn.cursor()    #print ("数据库打开成功")
                    sql = "UPDATE CoinWeb  SET (ip)  =  ('CDN') WHERE website = \""+str(host)+"\" "
                    #print(sql)
                    c.execute(sql)
                    conn.commit()
                    conn.close()
                elif len(result) == 1:   
                    for i in result:
                        print('[+]目标({})没用CDN服务！-------目标IP({})\n'.format(host,i.text))
                        '''
                        # 插入数据库
                        '''
                        conn = sqlite3.connect('coin.db')
                        c = conn.cursor()    #print ("数据库打开成功")
                        sql = "UPDATE CoinWeb SET(ip) =  (\""+str(i.text)+"\") where website = \""+str(host)+"\" "
                        c.execute(sql)
                        conn.commit()
                        conn.close()
                else:
                    print('error!')
            except:
                print('[-]连接异常!')

def get_domain():
        conn = sqlite3.connect('coin.db')
        c = conn.cursor()    #print ("数据库打开成功")
        sql = "SELECT website from CoinWeb "
        cursor = c.execute(sql)
        website = [row[0] for row in cursor]

        conn.commit()
        conn.close()

        return website

def getTargets():
    queue = Queue()
    website = get_domain()
    for host in website:
        queue.put(host)
    threads = []
    thread_count = 10
    for i in range(thread_count):
        threads.append(cdnScan(queue))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

getTargets()
