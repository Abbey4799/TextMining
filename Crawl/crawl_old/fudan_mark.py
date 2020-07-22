import requests
from requests.exceptions import RequestException
import json
import pymongo
import time


#headers of response
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
raw_cookies = "ASP.NET_SessionId=sg0yxyuk1la5551ltrprjlaf; Mycos_FD_O2ST=pgBkuqvYy7Md/ciG3Ao6UZ2GP4kDOlGNOXhOF4d5k8xjHlnbRoe7PQ==; amlbcookie=01; iPlanetDirectoryPro=LOGOUT; token=83D39FDFA67D6C73A133D770506792CF7AF1D88A030E7F114041A012E710591377383131071307E92F9A8C931C5C80B53E10677ADF087E9C4567880C3A68B9B738F535E05AB4B0B69CECC8D1D4E661922AD2F9EF18F137B0B886ED7AB6862DE5B280F6E7F445F69D95CA48CEBB9BA8CCF1E769E699AB37AC0DB6CD190DEADEDB7B2AA93E; user=7Ui6nZT3QrmHTl+3VFeMgA=="

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


