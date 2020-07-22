import requests
from requests.exceptions import RequestException
import json
import pymongo
import time


#headers of response
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
raw_cookies = "semester.id=202; JSESSIONID=72F7EC0CBF220AD8614E30566D2F4A4E.61-; iPlanetDirectoryPro=AQIC5wM2LY4SfcwJFSbQVjFE9y6Ddsg6l8BXt0jjFOsFXR0%3D%40AAJTSQACMDE%3D%23"

#send requests to the url and return json data
def get_one_page(url):
    cookies = {}
    for line in raw_cookies.split(';'):
        key,value=line.split('=',1)
        cookies[key]=value
    try:
        response = requests.get(url,cookies=cookies,headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except RequestException:
         print("抓取失败")

#analyze the json data and insert it into the mongoDB
def parse_one_page(d):
    try:
        datum = d['data']['ItemList']
        for data in datum:
            yield{
                'TeacherCode':data['TeacherCode'],
                'TeacherName':data['TeacherName'],
                'ClassCode':data['ClassCode'],
                'ClassName':data['ClassName'],
                'CourseCode':data['CourseCode'],
                'CourseName':data['CourseName'],
                'DepartmentCode':data['DepartmentCode'],
                'DepartmentName':data['DepartmentName'],
                'Semester':data['Semester'],
                'TaskGUID':data['TaskGUID'],
                'TaskName':data['TaskName'],
                'StudentCount':data['StudentCount'],
                'Score':data['Score'],
                'Median':data['Median'],
                'SelectPersonNum':data['SelectPersonNum'],
                'ClassAlias':data['ClassAlias']
            }
        if data['TeacherCode','TeacherName','ClassCode','ClassName','CourseCode','CourseName','DepartmentCode','DepartmentName','Semester','TaskGUID','TaskName','StudentCount','Score','Median','SelectPersonNum','ClassAlias'] == None:
            return None
    except Exception:
        return None
                                  

def main():
    #'psize' is the collections contained in one page
    #We know the total number, thus one page is enough
    #if you turn it into numbers larger than 1, the page can be changed automatically
    for i in range(1):
        url = 'http://ce.fudan.edu.cn/API/Students/QuestinlistByStu.ashx?action=queryresult&tasktype=5&semester=2018-2019-2&querycontent=&index={}&psize=7000&orderby=&col=&ordertype=&order='.format(i+1)
        d = get_one_page(url)
        # print('第{}页抓取完毕'.format(i+1))
        for item in parse_one_page(d):
            collection.insert_one(item)


if __name__=='__main__':
    #login in the DB mongo
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.local
    collection = db.Fudan
    
    #return the running time
    t0 = time.time()
    main()
    print(time.time() - t0)
    print("seconds wall time")


