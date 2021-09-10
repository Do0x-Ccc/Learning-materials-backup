#C/C++ 获取时间
int main() {
	time_t now;
	struct tm* tm_now;
	time(&now);
	tm_now = localtime(&now);//get date

	int year  = tm_now->tm_year + 1900;
	int month = tm_now->tm_mon + 1;
	int day   = tm_now->tm_mday;
	int hour  = tm_now->tm_hour;
	int min   = tm_now->tm_min;


	printf("start datetime: %d-%d-%d %d:%d\n", year, month, day, hour, min);

  # 将时间进行拼接
	int end_time = hour * 100 + min;
	printf("%d  \n", end_time);

	return 0;
}



