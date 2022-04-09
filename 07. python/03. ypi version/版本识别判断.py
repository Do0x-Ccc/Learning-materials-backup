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
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--headless')
                options.add_argument('blink-settings=imagesEnabled=false')
                options.add_argument('--disable-gpu')
    
                user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
                options.add_argument('user-agent={0}'.format(user_agent))
    
                driver = webdriver.Chrome(options=options)
    
                driver.get('{}'.format(host))
                time.sleep(5)
                bf = BeautifulSoup(driver.page_source, 'lxml')
                driver.quit()
                result = bf.find_all('div', class_='ant-col-6')
    
    
                result = result[3].find_all('a')
                result = result[0].text
                content = "域名: {}        {}".format(host,result)
                print(content)
                result_tmp = result.split('.')[1]
                if int(result_tmp) < 10 :
                    fo = open("result_this.txt", "a")
                    fo.write(content+"\n")
                    fo.close()
                    print(content+"     写入文件中。")
                
            except:
               print('[-]连接异常!')

def getTargets():
    queue = Queue()
    with open('targets.txt', 'r') as f:
        for i in f:
            host = i.rstrip('\n')
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
