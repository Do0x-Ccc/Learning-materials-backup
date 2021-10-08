if __name__ == '__main__':	
	while True:
		print("[-] 脚本运行中...")
		dt    = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')    	# 2021-10-08 12:49:53
		ts    = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))	# 时间转为时间戳
		#print(ts)

		dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') # 2021-10-08 12:49:53.441450  含微秒的日期时间，来源 比特量化
		dt_ms_sp = dt_ms.split('.',1);
		#print(dt_ms_sp[1])

		miaotime = str(ts)+"."+str(dt_ms_sp[1])
		print("[-] 当前时间戳...:  "+miaotime)

		time.sleep(0.0001)

		if int(dt_ms_sp[1]) < 10000:
			print("[*] 当前时间戳:"+miaotime+"    符合要求。")
			print(dt_ms_sp[1])
			exit();
