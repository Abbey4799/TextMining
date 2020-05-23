from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import pymongo
from sklearn.naive_bayes import MultinomialNB
from imblearn.over_sampling import SMOTE
from collections import Counter
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np

if __name__=='__main__':
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.local
    collection = db['manual_tagging']

    X=[] 
    Y=[]

    # 用评教分数训练
    
    for item in collection.find():
        X.append(item['comment_wihout_stpw'])
        if float(item['finalScore'])<=90:
            Y.append(0)
        else:
            Y.append(1)
    '''
    
    # 用snownlp训练
    
    for item in collection.find():
        X.append(item['comment_wihout_stpw'])
        if float(item['snownlp_score'])<=0.5:
            Y.append(0)
        else:
             Y.append(1)
    
    '''    
    '''
    # 用手工标注训练
    
    for item in collection.find():
        X.append(item['comment_wihout_stpw'])
        if int(item['snownlp_score'])==0:
            Y.append(0)
        else:
            Y.append(1)
    '''

    # 随机拿出数据集中20%的部分作为测试集
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=1)

    # 将X向量化并提取特征
    vertorizer=TfidfVectorizer(ngram_range=(1, 1),max_df=0.7,min_df=4,token_pattern=r"(?u)\b(?![0-9]+)\w\w+\b|\b(?![0-9]+)\w\+\w+\b")
    X_train_v=vertorizer.fit_transform(X_train)
    X_test_v=vertorizer.transform(X_test)
    print(vertorizer.get_feature_names())

    # SMOTE平衡样本（合成负评）
    print(Counter(Y_train))
    sm=SMOTE()
    X_sm,Y_sm=sm.fit_sample(X_train_v,Y_train)
    print(Counter(Y_sm))
    
    # 训练朴素贝叶斯并测试
    nb=MultinomialNB()
    nb.fit(X_sm,Y_sm)
    y_predict=nb.predict(X_test_v)
    
    print(metrics.classification_report(Y_test,y_predict))
    
    # 预测准确率
    accuracy=metrics.accuracy_score(y_predict,Y_test)
    print(accuracy)

    
    # ROC曲线绘制
    fpr,tpr,_=metrics.roc_curve(Y_test,y_predict,pos_label=1)
    auc=metrics.auc(fpr,tpr)

    # 中文和负号的正常显示
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 设置绘图风格
    plt.style.use('ggplot')
    # 绘制ROC曲线
    plt.plot(fpr, tpr, '')
    # 绘制参考线
    plt.plot((0, 1), (0, 1), 'r--')
    # 添加文本注释
    plt.text(0.5, 0.5, 'AUC=%.2f' % auc)
    # 设置坐标轴标签和标题
    plt.title('Multinomial naive bayes - ROC')
    plt.xlabel('1-specificity')
    plt.ylabel('Sensitivity')
    # 去除图形顶部边界和右边界的刻度
    plt.tick_params(top='off', right='off')
    # 图形显示
    plt.show()