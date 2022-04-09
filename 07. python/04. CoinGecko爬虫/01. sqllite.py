#!/usr/bin/python3

import sqlite3


##########
conn = sqlite3.connect('coin.db')
print ("数据库打开成功")
c = conn.cursor()


c.execute('''CREATE TABLE CoinAll
       (id     INTEGER PRIMARY KEY ,
       coin    TEXT    NOT NULL
                    ); ''')

c.execute('''CREATE TABLE CoinWeb
       (id        INTEGER PRIMARY KEY ,
       Coin_id    INT     NOT NULL,
       coin       TEXT,
       website    TEXT    NOT NULL,
       IP         TEXT,
       ascription TEXT
                    ); ''')
print ("数据表创建成功")
conn.commit()
conn.close()



conn = sqlite3.connect('coin.db')
c = conn.cursor()    #print ("数据库打开成功")

c.execute("INSERT INTO CoinAll (coin) VALUES  ('123.com')   ")
conn.commit()
conn.close()
