//创建一个替换的函数
//替换原文:	https://zhidao.baidu.com/question/277052495.html
void replace(char originalString[], char key[], char swap[]) {
	int lengthOfOriginalString, lengthOfKey, lengthOfSwap, i, j, flag;
	char tmp[1000];
	lengthOfOriginalString = strlen(originalString);
	lengthOfKey = strlen(key);
	lengthOfSwap = strlen(swap);
	for (i = 0; i <= lengthOfOriginalString - lengthOfKey; i++) {
		flag = 1;
		//搜索key
		for (j = 0; j < lengthOfKey; j++) {
			if (originalString[i + j] != key[j]) {
				flag = 0;
				break;
			}
		}
		if (flag) {
			strcpy(tmp, originalString);
			strcpy(&tmp[i], swap);
			strcpy(&tmp[i + lengthOfSwap], &originalString[i + lengthOfKey]);
			strcpy(originalString, tmp);
			i += lengthOfSwap - 1;
			lengthOfOriginalString = strlen(originalString);
		}
	}
}

int main(){
  
  //获取模块路径
	CHAR szPath[MAX_PATH] = { 0 };
	if (!GetModuleFileName(NULL, szPath, MAX_PATH))
	{
		printf("Cannot get the module file name, error: (%d) \n", GetLastError());
		return 1;
	}
	else {
		printf("Module file name: %s \n", szPath);
	}
	printf("%s \n", szPath); 
  
  
	char originalString[1000];       //定义新函数
	strcpy(originalString, szPath);  //将路径拷贝到字符串
	char key[] = {"000000.exe"};     //原来的字符串
	char swap[] = {"00000.exe"};     //替换后的字符串
	replace(originalString, key,swap);
	printf("%s", originalString);
  
  return 0;
}
