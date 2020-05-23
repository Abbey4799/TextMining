import jieba
import pymongo

def stopwords_list():
    stopword_list=[]
    with open("C:\\Users\\li_ya\\Desktop\\stopwords-master\\stopwords.txt","w",encoding='utf-8',errors='ignore') as f_s:
        with open("C:\\Users\\li_ya\\Desktop\\stopwords-master\\list1.txt","r",encoding='utf-8',errors='ignore') as f1:   # 百度停用词表
            for line in f1.readlines():
                if not line=="":
                    stopword_list.append(line.replace('\n',''))
        f1.close()
        
        with open("C:\\Users\\li_ya\\Desktop\\stopwords-master\\list2.txt","r",encoding='utf-8',errors='ignore') as f2:   # 哈工大停用词表
            for line in f2.readlines():
                if not line=="":
                    if not line in stopword_list:
                        stopword_list.append(line.replace('\n',''))
        f2.close()

        with open("C:\\Users\\li_ya\\Desktop\\stopwords-master\\list3.txt","r",encoding='utf-8',errors='ignore') as f3:   # 四川大学机器智能实验室停用词库
            for line in f3.readlines():
                if not line=="":
                    if not line in stopword_list:
                        stopword_list.append(line.replace('\n',''))
        f3.close()

        with open("C:\\Users\\li_ya\\Desktop\\stopwords-master\\list4.txt","r",encoding='utf-8',errors='ignore') as f4:
            for line in f4.readlines():
                if not line=="":
                    if not line in stopword_list:
                        stopword_list.append(line.replace('\n',''))
        f4.close()

        # 添加自定义的停用词表
        with open("C:\\Users\\li_ya\\Desktop\\stopwords-master\\list5.txt","r",encoding='utf-8',errors='ignore') as f5:
            for line in f5.readlines():
                if not line=="":
                    if not line in stopword_list:
                        stopword_list.append(line.replace('\n',''))
        f5.close()

        # 添加所有的课程名与老师名为停用词
        for item in name_collection.find():
            if not item['TeacherName'] in stopword_list:
                stopword_list.append(item['TeacherName'])
            if not item['CourseName'] in stopword_list:
                stopword_list.append(item['CourseName'])

        stopword_list.sort()
        f_s.writelines(stopword_list)
    f_s.close()
    stopword_list=set(stopword_list)
    print(stopword_list)
    return stopword_list

def move_stop_words(text):
    text_list_1=text.split(' ')
    text_list_2=[]
    for x in text_list_1:
        if not x in stopwords:
            text_list_2.append(x)
    return " ".join(text_list_2)

def chinese_word_cut(text):
    return " ".join(jieba.cut(text.replace(' ',''),cut_all=False))

def jieba_cut():    
    for item in comment_collection.find():
        item['comment_cut']=chinese_word_cut(item['comment'])
        item['comment_wihout_stpw']=move_stop_words(item['comment_cut'])
        comment_collection.save(item)

if __name__=='__main__':
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.local
    comment_collection = db['manual_tagging']
    name_collection = db['db_new']
    #comment_Wechat = db['Wechatcleaned']

    stopwords=stopwords_list()
    '''
    with open("C:\\Users\\li_ya\\Desktop\\userdict.txt","a",encoding='utf-8') as f_u:
        #f_u.write('\n')
        for item in comment_collection.find():
            f_u.write(item['TeacherName'])
            f_u.write('\n')
            f_u.write(item['CourseName'])
            f_u.write('\n')
    f_u.close()
    with open("C:\\Users\\li_ya\\Desktop\\userdict.txt","r",encoding='utf-8') as f_u:
        for line in f_u.readlines():
            print(line)
    f_u.close()
    '''
    jieba.load_userdict("C:\\Users\\li_ya\\Desktop\\userdict.txt")

    jieba_cut()