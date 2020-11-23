# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
from mpl_toolkits.axisartist.axislines import SubplotZero
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from data_utils import pkl_dump, pkl_load


# %%
init_path = 'outcomes_adaptive/'

# %% [markdown]
# # Bert

# %%
# model_names = ['bert_spec1','bert_spec2','lcf_bert1','lcf_bert2','aen1','aen2']


# %%
# train_out_raw = []
# test_out_raw = []
# for i in model_names:
#     train_out_raw.append(pkl_load(init_path, 'train_'+i))
#     test_out_raw.append(pkl_load(init_path, 'test_'+i))


# %%
# train_out_raw[0]


# %%
# train_out_acc = []
# train_out_f1 = []

# for model in train_out_raw:
#     temp_acc = []
#     temp_f1 = []
#     for i in model:
#         temp_acc.append(i[0])
#         temp_f1.append(i[1])
#     train_out_acc.append(temp_acc)
#     train_out_f1.append(temp_f1)


# %%
# np.array(train_out_acc).shape


# %%
# train_bert = np.array(train_out_acc)


# %%
# train_bert = np.array(train_out_acc)
# data_df=pd.DataFrame(train_bert)
# # create and writer pd.DataFrame to excel
# writer = pd.ExcelWriter('train_bert'+'.xlsx')  # 生成一个excel文件
# data_df.to_excel(writer,'page_1')  # 数据写入excel文件
# writer.save()  # 保存excel文件


# %%

# fig = plt.figure(1, (10, 6))

# ax = SubplotZero(fig, 1, 1, 1)
# fig.add_subplot(ax)

# """新建坐标轴"""
# ax.axis["xzero"].set_visible(True)

# """隐藏坐标轴"""
# ax.axis['bottom',"top",'right'].set_visible(False)

# #设置网格样式
# ax.grid(True, linestyle='-.')

# x = range(40)

# for idx,aa in enumerate(train_out_acc):
#     ax.plot(x,aa,'o-',label=model_names[idx])
# # ax.plot(x,rat_ave_airbnb,'o-',color = 'k',label="airbnb")#o-:圆形
# # ax.plot(x,rat_ave_cs,'o-',color = '#B44932',label="cs")#o-:圆形
# # ax.plot(x,rat_ave_github,'o-',color = '#5CB432',label="github")#o-:圆形
# # ax.plot(x,rat_ave_wiki,'o-',color = '#329DB4',label="wiki")#o-:圆形
# # ax.plot(x,rat_ave_fsq,'o-',color = '#8A32B4',label="fsq")#o-:圆形
# plt.xlabel("epoch")#横坐标名字
# plt.ylabel("auc")#纵坐标名字
# plt.legend(loc = "best")#图例
# plt.show()


# %%

# fig = plt.figure(1, (10, 6))

# ax = SubplotZero(fig, 1, 1, 1)
# fig.add_subplot(ax)

# """新建坐标轴"""
# ax.axis["xzero"].set_visible(True)

# """隐藏坐标轴"""
# ax.axis['bottom',"top",'right'].set_visible(False)

# #设置网格样式
# ax.grid(True, linestyle='-.')

# x = range(40)

# for idx,aa in enumerate(train_out_f1):
#     ax.plot(x,aa,'o-',label=model_names[idx])
# # ax.plot(x,rat_ave_airbnb,'o-',color = 'k',label="airbnb")#o-:圆形
# # ax.plot(x,rat_ave_cs,'o-',color = '#B44932',label="cs")#o-:圆形
# # ax.plot(x,rat_ave_github,'o-',color = '#5CB432',label="github")#o-:圆形
# # ax.plot(x,rat_ave_wiki,'o-',color = '#329DB4',label="wiki")#o-:圆形
# # ax.plot(x,rat_ave_fsq,'o-',color = '#8A32B4',label="fsq")#o-:圆形
# plt.xlabel("epoch")#横坐标名字
# plt.ylabel("f1")#纵坐标名字
# plt.legend(loc = "best")#图例
# plt.show()


# %%
# test_out_raw

# %% [markdown]
# # non-BERT

# %%
model_names = ['mgan','aoa','tnet_lf','cabasc','ian','atae_lstm','td_lstm','tc_lstm','lstm']
# model_names = ['mgan'，'aoa']


# %%
train_out_raw = []
test_out_raw = []
for i in model_names:
    train_out_raw.append(pkl_load(init_path, 'train_'+i))
    test_out_raw.append(pkl_load(init_path, 'test_'+i))


# %%
train_out_acc = []
train_out_f1 = []

for model in train_out_raw:
    temp_acc = []
    temp_f1 = []
    for i in model:
        temp_acc.append(i[0])
        temp_f1.append(i[1])
    train_out_acc.append(temp_acc)
    train_out_f1.append(temp_f1)



# %%
test_out_acc = []
test_out_f1 = []

for model in test_out_raw:
    test_out_acc.append(model[0][0])
    test_out_f1.append(model[0][1])



# %%

fig = plt.figure(1, (20, 6))

ax = SubplotZero(fig, 1, 1, 1)
fig.add_subplot(ax)

"""新建坐标轴"""
ax.axis["xzero"].set_visible(True)

"""隐藏坐标轴"""
ax.axis['bottom',"top",'right'].set_visible(False)

#设置网格样式
ax.grid(True, linestyle='-.')

x = range(len(train_out_acc[0]))

for idx,aa in enumerate(train_out_acc):
    ax.plot(x,aa,'o-',label=model_names[idx])
# ax.plot(x,rat_ave_airbnb,'o-',color = 'k',label="airbnb")#o-:圆形
# ax.plot(x,rat_ave_cs,'o-',color = '#B44932',label="cs")#o-:圆形
# ax.plot(x,rat_ave_github,'o-',color = '#5CB432',label="github")#o-:圆形
# ax.plot(x,rat_ave_wiki,'o-',color = '#329DB4',label="wiki")#o-:圆形
# ax.plot(x,rat_ave_fsq,'o-',color = '#8A32B4',label="fsq")#o-:圆形
plt.xlabel("epoch")#横坐标名字
plt.ylabel("auc")#纵坐标名字
plt.legend(loc = "best")#图例
plt.show()


# %%
len(train_out_acc[0])


# %%

fig = plt.figure(1, (10, 6))

ax = SubplotZero(fig, 1, 1, 1)
fig.add_subplot(ax)

"""新建坐标轴"""
ax.axis["xzero"].set_visible(True)

"""隐藏坐标轴"""
ax.axis['bottom',"top",'right'].set_visible(False)

#设置网格样式
ax.grid(True, linestyle='-.')

x = range(len(train_out_acc[0]))

for idx,aa in enumerate(train_out_f1):
    ax.plot(x,aa,'o-',label=model_names[idx])
# ax.plot(x,rat_ave_airbnb,'o-',color = 'k',label="airbnb")#o-:圆形
# ax.plot(x,rat_ave_cs,'o-',color = '#B44932',label="cs")#o-:圆形
# ax.plot(x,rat_ave_github,'o-',color = '#5CB432',label="github")#o-:圆形
# ax.plot(x,rat_ave_wiki,'o-',color = '#329DB4',label="wiki")#o-:圆形
# ax.plot(x,rat_ave_fsq,'o-',color = '#8A32B4',label="fsq")#o-:圆形
plt.xlabel("epoch")#横坐标名字
plt.ylabel("f1")#纵坐标名字
plt.legend(loc = "best")#图例
plt.show()



# %%
train_wsw = np.array(train_out_acc)
train_wsw = train_wsw.round(3)
data_df=pd.DataFrame(train_wsw)
# create and writer pd.DataFrame to excel
writer = pd.ExcelWriter('out_data/train_adaptive'+'.xlsx')  # 生成一个excel文件
# writer = pd.ExcelWriter('out_data/train_glove_review_wosw2'+'.xlsx')  # 生成一个excel文件
data_df.to_excel(writer,'page_1')  # 数据写入excel文件
writer.save()  # 保存excel文件



ll = len(test_out_acc)
test_out_acc = np.array(test_out_acc)
test_wsw = test_out_acc.reshape(1,ll)
test_wsw = test_wsw.round(3)
data_df=pd.DataFrame(test_wsw)
# create and writer pd.DataFrame to excel
writer = pd.ExcelWriter('out_data/test_adaptive'+'.xlsx')  # 生成一个excel文件
# writer = pd.ExcelWriter('out_data/test_glove_review_wosw2'+'.xlsx')  # 生成一个excel文件
data_df.to_excel(writer,'page_1')  # 数据写入excel文件
writer.save()  # 保存excel文件

