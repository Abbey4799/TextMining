#-*- coding: utf-8 -*-
import pymongo
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import getopt
import sys
from matplotlib.font_manager import _rebuild

def scatter():
    fig = plt.figure(1)
    fig.set_figwidth(20)
    fig.set_figheight(5)
    marks = []
    count = []
    marks_print = []
    bar = []
    xx = 0
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    for item in original_collection.find():
        if(item['finalScore']==0):
            continue
        num = (float(item['finalScore']) - 40)/60.0 * 100
        if num < 60:
            a = a+1
        elif num > 60 and num < 70:
            b = b+1
        elif num > 70 and num < 80:
            c = c+1
        elif num > 80 and num < 90:
            d = d+1
        elif num > 90 and num < 101:
            e = e+1
        marks.append(num)
        count.append(xx)
        xx = xx+1
    marks_print = sorted(marks)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    x = np.array(count)
    y = np.array(marks_print)
    bar = [a,b,c,d,e]
    name = ['<60','60~70','70~80','80~90','90~100']
    plt.title('分数分布')
    plt.bar(range(len(bar)), bar, tick_label=name, color = '#F08080')
    plt.show()

    
    
    ax1.set_title('分数分布')
    plt.xlabel('X')
    plt.ylabel('Y')
    ax1.scatter(x,y,c = '#F08080',marker = '.')
    plt.legend('x1')
    plt.xlabel('被评教课程编号')
    plt.ylabel('分数（放大比例后）')
    plt.show()

if __name__ == '__main__':
    _rebuild()
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.local
    original_collection = db['db_new']
    scatter()
