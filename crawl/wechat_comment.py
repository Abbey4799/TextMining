from selenium import webdriver
import time
import json
import random
import requests
import re
import pymongo
import bs4

#if para selected by BeautifulSoup contains these words
# the searching process will be terminated
stopwords = ['已发送','http','有想要','长按二维码','復小七','喜欢的话就关注我们','jwfw.fudan.edu.cn']

#the headers for requests
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
raw_cookies = "RRK=GEq8Myy5fE; ptcz=cb3c543b018bf7162c0f17094055bce5c4ab355c891676b59b6a87107afe2363; pgv_pvid=9252277167; pgv_pvi=1232247808; XWINDEXGREY=0; tvfe_boss_uuid=3076e3bc67d27a43; o_cookie=547809343; ua_id=piecxRkDQ9L2JG1WAAAAAMOOvYMNxf-zKlO-N7l2F-I=; mm_lang=zh_CN; wxuin=69220869317680; pac_uid=1_547809343; pgv_si=s4713364480; cert=4uEA3_aNIgf8Joyc_9CukrtY7uKqZ2ig; noticeLoginFlag=1; xid=; openid2ticket_op4g0w9SYe3GlGQRlDU8GdZIIZmg=g/C/HqjBPlTRjauz/4IQitJ265U+tmNnylJGcJpnlic=; rewardsn=; wxtokenkey=777; openid2ticket_oUzdV4-qcHzK8yPSvZ1UXgh9Tb8w=mVSxBFLGauyZpj/3/EQCxFxieqYRJuruUO52As96P2I=; ticket=7597baf3cb2c2a1d79c679f142e60979a7d4a966; ticket_id=gh_4f37e6ba20e7; uuid=86eeb2cf1b6e52a7c250194d79bffe93; data_bizuin=3510833855; bizuin=3525833369; data_ticket=VqijWmsOGrU6teNXnpPc8oldOeAgFC/S6W8EJ712A4quWfJ9Q/TCYUzQwVdDyiQ6; slave_sid=cjdIdjRwNWZFY1VGNFlSSXR0X1ZaX2Ntd0hYa2pXMFNNQkJkMjByNTdzcENQT2RuZUNQMWhnQnVqTmRrdUh6N1hhcWdwRGJrc25kbTZjcnRjV0J2N0l0ZUtnQTZadmQyNEJlVWpHcDBkVDUyWEpiV3ltTHBxUEFGb21BdmNEd2kzNkFnYTFQbkJGODVOTDVi; slave_user=gh_4f37e6ba20e7; openid2ticket_ovxJD0dqP5fRpgrpTtAsTw0otNt4=ZerWYMh+gj304llA7OzhA4Vo0RvOfhdRo3wyC4yeDGU="


#get the comments for every article in FuXiaoDan
#the whole process can be broken into three parts
#1. Elementary setting ( get headers/cookies/Session/token)
#2. Enter the 'FuXiaoDan'
#3. Get the link of every articles
def getGZH(query):
#1. Elementary setting ( get headers/cookies/Session/token)
    url = 'https://mp.weixin.qq.com'

    # set headers for requests
    header = {
        "HOST": "mp.weixin.qq.com",
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }

    # read cookies
    cookies = {}
    for line in raw_cookies.split(';'):
        key,value=line.split('=',1)
        cookies[key]=value

    # increase the retry times for building session
    session = requests.Session()
    session.keep_alive = False
    session.adapters.DEFAULT_RETRIES = 511
    time.sleep(5)

    # get token
    response = session.get(url=url, cookies=cookies, verify=False)
    token = re.findall(r'token=(\d+)', str(response.url))[0]
    time.sleep(2)

#2. Enter the 'FuXiaoDan'
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
    # search 'FuXiaoDan'
    query_id = {
        'action': 'search_biz',            #行为为搜索
        'token': token,                    #搜索行为需要标识符
        'lang': 'zh_CN',                   #中文
        'f': 'json',                       #形式为json数据
        'ajax': '1',
        'random': random.random(),         #任意随机数
        'query': query,                    #请求的公众号名称
        'begin': '0',                      #从第0页开始
        'count': '5'                       #每页5个
    }
    GZH_response = session.get(
                           search_url,
                           cookies=cookies,
                           headers=header,
                           params=query_id)
    # 'FuXiaoDan' is the first of the lists
    lists = GZH_response.json().get('list')[0]
    #get fake id of 'FuXiaoDan'
    fakeid = lists.get('fakeid')

#3. Get the link of every articles
    appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
    # Search every articles
    query_id_data = {
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'action': 'list_ex',
        'begin': '0',
        'count': '5',
        'query': '',
        'fakeid': fakeid,
        'type': '9'
    }
    appmsg_response = session.get(
                                  appmsg_url,
                                  cookies=cookies,
                                  headers=header,
                                  params=query_id_data)
    # Get the total number of articles
    max_num = appmsg_response.json().get('app_msg_cnt')
    begin = 0
    # the number of pages
    num = int(int(max_num) / 5)

    articles = []

    while num + 1 > 0:
        query_id_data = {
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '{}'.format(str(begin)),
            'count': 5,
            'query': '',
            'fakeid': fakeid,
            'type': '9'
        }
        print('*********flip over the page**********',begin)
        time.sleep(5)

        #get the page
        query_fakeid_response = requests.get(
                                             appmsg_url,
                                             cookies=cookies,
                                             headers=header,
                                             params=query_id_data)
        print(query_fakeid_response.json())
        # get the articles of this page
        fakeid_list = query_fakeid_response.json().get('app_msg_list')
        if fakeid_list:
            for item in fakeid_list:
                content_link = item.get('link')
                content_title = item.get('title')
                article = {}
                article['CourseName'] = content_title
                article['link'] = content_link
                articles.append(article)
        num -= 1
        begin = int(begin)
        begin += 5
    # return all the articles of this page to insert into the mongoDB
    return articles

#Clean the title
def clean_title(title):
    stop = ['：']
    stopwords = ['|','丨','|','｜']
    for item in stop:
        if title.find(item) > -1:
            index = title.find(item)
            title = title[index+1:]
    for item in stopwords:
        if title.find(item) > -1:
            index = title.find(item)
            title = title[index+1:]
    title = title.replace('「','').replace('」','').replace(' ','')
    return title


#Get the comment
def get_comment(query):
    #Now we have every link of the articles
    articles = []
    articles = getGZH(query)
    for item in articles:
        item['CourseName'] = clean_title(item['CourseName'])
        item['comment'] = ""
        response = requests.get(item['link'])
        if response is not None:
            html = bs4.BeautifulSoup(response.text, 'html.parser')
            #Find the <p></p>
            paragraphs = html.select("p")
            flag = 0
            for para in paragraphs:
                #Start record the comment whenever para contains the word 'comment'
                if para.text.find('评价') > -1:
                    flag = 1
                if flag == 1:
                    #stop when encountered the para with stopwords
                    temp = 0
                    for word in stopwords:
                        if para.text.find(word) > -1:
                            temp = 1
                            break
                    if temp == 1:
                        break
                    #if para doesn't contain stop words
                    item['comment'] += para.text
        collection.insert_one(item)


if __name__ == '__main__':
    #Log in the mongoDB
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.local
    collection = db.Wechat

    #Log in the 'FuXiaoQi'
    #get comments
    query = "復小七" #'FuXiaoQi'
    print("Start：" + query)
    get_comment(query)
    print("Finished!")



