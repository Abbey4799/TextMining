import pymongo
import csv
import numpy as np
import pandas as pd
import getopt
import sys

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.local
original_collection = db['db_new']

columns = ['DepartmentName','CourseName','TeacherName','Score','Median','finalScore','SelectPersonNum']
columns_name = ['开课院系','课程名','教师','平均分','中位数','最终得分','有效问卷数']

array_1 = ['古典诗词导读',
'中国当代小说选读',
'宋词导读',
'诗经与传统文化',
'《红楼梦》与人生',
'中国现代散文导读',
'中国现代文学名著选讲',
'《论语》导读',
'《老子》导读',
'《春秋》三传选读']

array_2 = ['笛卡尔《谈谈方法》导读',
'《共产党宣言》导读',
'康德《实践理性批判》精读',
'康德《实践理性批判》精读',
'《论法的精神》导读',
'《法哲学原理》导读',
'《查拉图斯特拉如是说》导读',
'《费尔巴哈论》研读',
'艺术哲学与审美问题',
'批判性思维与论证问题',
'托克维尔论美国的民主',
'亚里士多德《政治学》导读']
array_3 = ['莎士比亚作品撷英',
           '基督教文明史',
           '性别与历史',
           '日本文明的历史变迁',
           '古代近东的英雄与神祇',
           '古希腊神话',
           '20世纪的中美关系与东亚世界',
           '古代中国的海洋文明',
           '希伯来圣经']
array_4 = ['经济与社会',
'人权与法',
'宪政文明史',
'法治理念与实践',
'法律与科技文明',
'全球化时代的法律冲突与对话',
'法律与社会',
'文化与社会']

array_5 = ['化学与人类',
'从计算到智能',
'计算思维',
'信号、信息与社会',
'无处不在的大分子',
'航空与航天']

array_6 = ['生命进化论',
'微生物与人类健康',
'身边的基因科学',
'人类进化',
'环境与人类',
'环境灾害与启示',
'走近医学：历史与传承',
'药物·生命·社会',
'社会发展与健康',
'改变世界的流行病']

array_7 = ['中国戏曲·京剧',
'陶艺与雕塑',
'戏剧经典与表达·西方戏剧',
'达芬奇笔记与绘画实践',
'西方古典建筑',
'欧洲电影解析与实践',
'文物赏析与体验',
'考古与人类',
'西方现代艺术：历史与理论',
'影视剧艺术',
'校园歌曲赏析和创作',
'当代电影美学',
'中外音乐审美',
'数码钢琴演奏（初级）',
'中外电影比较研究',
'世界民族音乐文化',
'美学与人生',
'中外建筑与环境艺术',
'构成艺术与设计思维',
'构成艺术与设计思维',
'数码艺术设计基础',
'新媒体艺术',
'数字动画艺术与设计',
'外国代表性舞蹈表演与赏析',
'建筑空间艺术之旅',
'音乐美学与实践',
'影片精读：方法与实践',
'影片精读：方法与实践',
'中国民族民间舞表演与赏析',
'素描',
'写生',
'微电影与微时代',
'微影人的自我修养',
'合唱与指挥',
'戏剧表演',
'古琴艺术导赏与演奏入门',
'原本性音乐教育与社区服务',
'数字影像艺术',
'合唱作品赏析与实践（中级）',
'虚拟空间设计与表现']

array_mokuai = [array_1,array_2,array_3,array_4,array_5,array_6,array_7]

k = 0
for count in array_mokuai:
    k = k + 1
    user_file_name = './第' + str(k) + '模块.xls'
    query = {}
    query['CourseName'] = {'$in':count}

    data = []
    for item in original_collection.find(query).sort('finalScore',-1):
        temp_data = []
        for i in columns:
            temp_data.append(' ')
        for key in item.keys():
            if key == '_id':
                continue
            index = columns.index(key)
            temp_data[index] = str(item[key])
        data.append(temp_data)
    data = pd.DataFrame(data)
    data.columns = columns_name

    data.to_excel(user_file_name,index=False)


