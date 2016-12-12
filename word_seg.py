# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#读取字典
def load_dic(filename):
    f = open(filename, 'r')#读取字典文件
    word_dic = set()#设置一个集合类似list但是是无序的
    max_length = 1#设置一个默认的词语最大长度
    for line in f:#遍历字典文件
        word = unicode(line.strip('\n'),'utf8')#删除末尾\n，并用转成utf8的字符编码
        #word = word.strip()
        word = word.split()#用空格作为标记 将 后面的字符串变成 list AT&T 3 nz 这个用的jieba 的字典
        word_dic.add(word[0])#将字典载入到集合
        if len(word[0]) > max_length:#如果list中的字典长度大于默认则修改为list中字典的长度
            max_length = len(word[0])
    return max_length, word_dic#返回字典中词的最大长度和集合

#中文分词算法之最大正向匹配算法
def fmm_word_seg(sentence, word_dic, max_length):
    sentence = unicode(sentence, 'utf8')#将句子的字符集编码变成utf8
    begin = 0#设置一个起始位置
    words = []#保存返回的分词后的字符串list
    count1_all = 0 #正向分词结果总词数
    count1_single = 0 #正向分词结果单字词数

    while begin < len(sentence):#遍历句子
    #for i in range（5,0,-1）表示i 5,4,3,2,1
    #min(begin + max_len, len(sentence))防止begin + max_len越界
        for end in range(min(begin + max_length, len(sentence)), begin, -1):
            #sentence[begin : end]切片
            #a = '123' a[0:2]->'12'
            word = sentence[begin : end]#取出 begin : end 的字符串
            if word in word_dic or end == begin + 1:#如果字符在字典中存在或者只有一个字符则进入下面的步骤
                words.append(word)#将字符串保存到words中
                count1_all = count1_all + 1
                if end == begin + 1:
                    count1_single = count1_single + 1
                break#跳出for循环
        begin = end#修改起始位置
    return words, count1_all, count1_single#返回


#中文分词算法之最大逆向匹配算法
def rmm_word_seg(sentence, word_dic, max_length):
    sentence = unicode(sentence, 'utf8')
    end = len(sentence)
    words = []
    count2_all = 0 #反向分词结果总词数
    count2_single = 0 #反向分词结果单字词数
    
    while end > 0:
         for begin in range(max(end - max_length, 0), end, 1):
        # for i in range(0,5,1) 输出的i依次是0,1,2,3,4
             word = sentence[begin : end]
             if word in word_dic or begin == end - 1:
                 words.insert(0, word)#words.append(word)将倒序字符串保存到words中
                 count2_all = count2_all + 1
                 if begin == end - 1:
                    count2_single = count2_single + 1
                 break
         end = begin
    return words, count2_all, count2_single
  
'''
规则：
 1.如果正反向分词结果词数不同，则取分词数量较少的那个。

    2.如果分词结果词数相同

                 a.分词结果相同，就说明没有歧义，可返回任意一个。

                 b.分词结果不同，返回其中单字较少的那个。

#中文分词算法之双向匹配算法
def bmm_word_seg(fmm, rmm): #fmm是调用正向分词的函数结果列表，rmm为反向分词的函数结果列表
    if fmm[1] != rmm[1]:
       if fmm[1] < rmm[1] :
           return fmm[0]
       else:
           return rmm[0]
    else:
        if fmm[0] == rmm[0]:
            return fmm[0]
        else:
            if fmm[2] < rmm[2]:
                return fmm[0]
            else:
                return rmm[0]
'''
#中文分词算法之双向匹配算法
def bmm_word_seg(fmm, rmm): #fmm是调用正向分词的函数结果列表，rmm为反向分词的函数结果列表
    bmm_words = []
    
    if fmm[1] != rmm[1]:
       if fmm[1] < rmm[1] :
           bmm_words = fmm[0]
       else:
           bmm_words = rmm[0]
    else:
        if fmm[0] == rmm[0]:
            bmm_words = fmm[0]
        else:
            if fmm[2] < rmm[2]:
                bmm_words = fmm[0]
            else:
                bmm_words = rmm[0]
    return bmm_words

#中文分词算法之全分法
def fullmm_word_seg(sentence, word_dic, max_length):
    sentence = unicode(sentence, 'utf8')#将句子的字符集编码变成utf8
    begin = 0#设置一个起始位置
    words = []#保存返回的分词后的字符串list

    while begin < len(sentence):#遍历句子
    #for i in range（5,0,-1）表示i 5,4,3,2,1
    #min(begin + max_len, len(sentence))防止begin + max_len越界
'''
        for end in range(min(begin + max_length, len(sentence)), begin, -1):
            #sentence[begin : end]切片
            #a = '123' a[0:2]->'12'
            word = sentence[begin : end]#取出 begin : end 的字符串
            if word in word_dic:#如果字符在字典中存在或者只有一个字符则进入下面的步骤
                words.append(word)#将字符串保存到words中
            else:
                if end == begin + 1:
                    words.append(word)#将字符串保存到words中
                    break#跳出for循环
        begin = end#修改起始位置
'''
        for i in range(0, max_length, 1):
            i = i + 1
            end = begin + i
            word = sentence[begin : end]
            if word in word_dic:
                words.append(word)
    return words#返回



sentence = '我在研究生命起源，学校再不发钱我就要吃土'
max_length, word_dic = load_dic('dict.txt')
a = fmm_word_seg(sentence, word_dic, max_length)
b = rmm_word_seg(sentence, word_dic, max_length)
c = bmm_word_seg(a, b)
print 'fmm_word_seg:' + ('/').join(a[0])
print 'rmm_word_seg:' + ('/').join(b[0])
print 'fmm_word_seg_all:', a[1], '   fmm_word_seg_single:', a[2]
print 'rmm_word_seg_all:', b[1], '   rmm_word_seg_single:', b[2]
print 'bmm_word_seg:' + ('/').join(c)


'''
print '正向分词：' + ('/').join(a[0])
print '逆向分词：' + ('/').join(b[0])
print '正向分词总词数:', a[1], '正向分词单字总数：', a[2]
print '逆向分词总词数', b[1], '逆向分词单字总数：', b[2]
print '双向分词总词数：' + ('/').join(c)
'''

