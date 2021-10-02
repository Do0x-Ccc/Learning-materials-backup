#encoding =utf-8
import itertools
import string

'''
String模块中的常量：
string.digits：数字0~9
string.ascii_letters：所有字母（大小写）
string.lowercase：所有小写字母
string.printable：可打印字符的字符串
string.punctuation：所有标点
string.uppercase：所有大写字母
'''
num_list = list(string.digits)


# itertools模块，生成列表, 例如 [1,2,3,4]
def permute(nums):
        from itertools import permutations
        result = []
        # permutations(nums,4): 第二个参数4就是你要生成的位数，你要生成几位?
        for i in permutations(nums,4):
            result.append(list(i))
        return result

# 列表变为数字 1234
num_list_res  = permute(num_list)

for a in num_list_res:
    # join用法: 说list包含数字，不能直接转化成字符串。     JOIN非数字: print(' '.join(list1))      JSON包含数字: print(''.join('%s' %id for id in a))
    print(''.join('%s' %id for id in a))
    '''
    wenben = ''.join('%s' %id for id in a)
    f = open('test.txt', 'a+')
    f.write(wenben+"\r\n")
    f.close()
    '''
