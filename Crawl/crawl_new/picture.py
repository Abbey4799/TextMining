# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import requests
from requests.exceptions import RequestException
import json
import pymongo
import time
import re
import bs4
import threading
import numpy as np
from matplotlib import font_manager as fm
import matplotlib.pyplot as plt
from  matplotlib import cm
import seaborn as sns
import copy


# %%
if __name__=='__main__':
    #login in the DB mongo
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.review
    collection_new = db.deal


# %%
def combine():
    # # 合并相同的课程（老师相同）
    arr = collection.find()
    for item in arr:
        new_item = copy.deepcopy(item)
        idd = new_item['_id']
        new_item.pop('_id')
        fd = {}
        fd['ClassName'] = new_item['ClassName']
        fd['TeachaerName'] = new_item['TeachaerName']
        for item1 in collection.find(fd):
            if item1['_id'] == idd:
                continue
            new_item["pstcmt"] += item1["pstcmt"]
            new_item["ngtcmt"] += item1["ngtcmt"]
        flag = 0
        for item1 in collection_new.find(fd):
            flag = 1
        if flag == 0:
            collection_new.insert_one(new_item)

    # # 合并相同的课程（老师相同）
#     collection_new = db.deal
#     arr = collection_new.find()
#     for item in arr:
#         idd = item['_id']
#         fd = {}
#         fd['ClassName'] = item['ClassName']
#         fd['TeachaerName'] = item['TeachaerName']
#         for item1 in collection_new.find(fd):
#             if item1['_id'] == idd:
#                 continue
#             collection_new.delete_one(item1)


# %%
# combine()

# %% [markdown]
# ## 合并后绘图

# %%
collection_new.count()
arr = collection_new.find()

pst_sum = 0
ngt_sum = 0
pst_len = {}
ngt_len = {}
pst_hist = []
ngt_hist = []
for item in arr:
    temp = len(item["pstcmt"])
    pst_sum += temp
    pst_hist.append(temp)
    if str(temp) not in pst_len:
        pst_len[str(temp)] = 0
    pst_len[str(temp)] += 1
    
    temp = len(item["ngtcmt"])
    ngt_sum += temp
    ngt_hist.append(temp)
    if str(temp) not in ngt_len:
        ngt_len[str(temp)] = 0
    ngt_len[str(temp)] += 1
# print(pst_len)
# print(ngt_len)
print(pst_sum)
print(ngt_sum)


# %%
a = []
b = []
for i in range(40):
    if str(i) in pst_len:
        a.append(pst_len[str(i)])
    else:
        a.append(0)
for i in range(40):
    if str(i) in ngt_len:
        b.append(ngt_len[str(i)])
    else:
        b.append(0)


# %%
c = np.array(a) + np.array(b)
c


# %%
plt.bar(np.linspace(1,len(a),len(a)), a)
plt.xlabel('Num of Postive Reviews',fontsize=20)
plt.ylabel('Num of classes',fontsize=20)
plt.grid(axis='both')
# legend = plt.legend(loc="upper left",fontsize=20) # label的位置在左上，没有这句会找不到label去哪了
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.show()


plt.bar(range(0, len(b)), b)
plt.xlabel('Num of Negative Reviews',fontsize=20)
plt.ylabel('Num of classes',fontsize=20)
plt.grid(axis='both')
# legend = plt.legend(loc="upper left",fontsize=20) # label的位置在左上，没有这句会找不到label去哪了
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.show()

plt.bar(range(0, len(c)), c)
plt.xlabel('Num of ALL Reviews',fontsize=20)
plt.ylabel('Num of classes',fontsize=20)
plt.grid(axis='both')
# legend = plt.legend(loc="upper left",fontsize=20) # label的位置在左上，没有这句会找不到label去哪了
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.show()


# %%
fig, ax = plt.subplots(figsize=(8, 4))
bins = 1000000
# Overlay a reversed cumulative histogram.
ax.hist(pst_hist, bins=bins, density=True, histtype='step', cumulative=True,
        label='Reversed emp.')



plt.xlim(0, 150)
# tidy up the figure
ax.grid(True)
ax.legend(loc='right')
ax.set_title('Postive Review - Cumulative step histograms')
ax.set_xlabel('Num of Review')
ax.set_ylabel('Num of Courses')

plt.show()

fig, ax = plt.subplots(figsize=(8, 4))
bins = 1000000
# Overlay a reversed cumulative histogram.
ax.hist(ngt_hist, bins=bins, density=True, histtype='step', cumulative=True,
        label='Reversed emp.')



plt.xlim(0, 150)
# tidy up the figure
ax.grid(True)
ax.legend(loc='right')
ax.set_title('Negative Review - Cumulative step histograms')
ax.set_xlabel('Num of Review')
ax.set_ylabel('Num of Courses')

plt.show()


# %%
a = [1,2]
b = copy.deepcopy(a)
a = [1,3]
a,b


# %%
a = {'1':1}
a.pop('1')
a

# %% [markdown]
# ### 评论长度分布

# %%
collection_new.count()
arr = collection_new.find()

pst_len_hist = []
ngt_len_hist = []
pst_len = 0
ngt_len = 0
pst_test = []
ngt_test = []

for item in arr:
    for _ in item["pstcmt"]:
        pst_len_hist.append(len(_))
        if len(_)>10 and len(_)<25:
            pst_len += 1
            pst_test.append(_)
    for _ in item["ngtcmt"]:
        ngt_len_hist.append(len(_))
        if len(_)>10 and len(_)<25:
            ngt_len += 1
            ngt_test.append(_)
        
        


# %%
pst_test[100:200]


# %%
# pst_test_tmp = [line+'\n' for line in pst_test]
# f = open('../../data/positive.txt','w')
# f.writelines(pst_test_tmp) 
# f.close()


# %%
len(pst_test)


# %%
ngt_test[:100]


# %%
len(ngt_test)


# %%
ngt_test_tmp = [line+'\n' for line in ngt_test]
f = open('../../data/negative.txt','w')
f.writelines(ngt_test_tmp) 
f.close()


# %%
pst_len,ngt_len


# %%
fig, ax = plt.subplots(figsize=(8, 4))
bins = 200
# Overlay a reversed cumulative histogram.
ax.hist(pst_len_hist, bins=bins, density=True, histtype='step',
        label='Reversed emp.')



plt.xlim(0, 50)
# tidy up the figure
ax.grid(True)
ax.legend(loc='right')
ax.set_title('Postive Review - Cumulative step histograms')
ax.set_xlabel('Length of Review')
ax.set_ylabel('Percentage of Reviews')

plt.show()


fig, ax = plt.subplots(figsize=(8, 4))
bins = 200
# Overlay a reversed cumulative histogram.
ax.hist(ngt_len_hist, bins=bins, density=True, histtype='step',
        label='Reversed emp.')



plt.xlim(0, 50)
# tidy up the figure
ax.grid(True)
ax.legend(loc='right')
ax.set_title('Negative Review - Cumulative step histograms')
ax.set_xlabel('Length of Review')
ax.set_ylabel('Percentage of Reviews')

plt.show()


# %%



