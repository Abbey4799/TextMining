import os
import time
import numpy as np
import pandas as pd
from pandas import DataFrame,Series
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import copy
import logging

import helper_model


def normalize(Data):
    newData = []
    for i in Data:
        if sum(i) == 0:
            newData.append(i)
        else:
            newData.append(i/np.sum(i))
    return np.array(newData)



'''
log_path = "logs/.log"
if not os.path.exists("logs/"):
    utils.makedirs("logs/")
logger = get_logger(logpath=log_path)
logger.info(str(time.asctime( time.localtime(time.time()) )))
'''

class TCHN(object):
    
    def __init__(self,maxNumberGlobalIterations=100,maxNumberLocalIterations=100,errorCorrectionRate=0.1,minError=0.01):
        self.maxNumberGlobalIterations = maxNumberGlobalIterations
        self.maxNumberLocalIterations = maxNumberLocalIterations
        self.errorCorrectionRate = errorCorrectionRate
        self.minError = minError
        self.numIterations = 0
        self.fbridge = np.zeros((numTerms,numClasses))
        self.fTest = np.zeros((numTest,numClasses))
        
    
    def classifyInstance(self,weightMatrix):
        '''
        利用与sample相连的bridge objects的classvalue，更新该sample的class
        input: [numTrain * numTerms] 一个sample的bridge objects
        return: [numTrain * numclasses]
        '''
        
        # equation 33
        classes = np.dot(weightMatrix,self.fbridge)

        newclasses = []
        
        for i in classes:
            # 如果classes[i]的值小于0，则集体偏移
            if min(i) < 0:
                i += abs(min(i))

            if np.sum(i) == 0:
                newclasses.append(i)
            else:
                newclasses.append(i/np.sum(i))

        return np.array(newclasses)
        
    def classifyInstanceReal(self,weightMatrix):
        '''
        利用与sample相连的bridge objects的classvalue，更新该sample的class
        input: [numTrain * numTerms] 一个sample的bridge objects
        return: [numTrain * numclasses]
        '''
        
        # equation 33
        # print(weightMatrix[0])
        # print(self.fbridge[:,0])
        classes = np.dot(weightMatrix,self.fbridge)
        # print(classes[0])

        return classes
        
    def train(self):
        log_path = "logs/test.log"
        if not os.path.exists("logs/"):
            utils.makedirs("logs/")
        logger = helper_model.get_logger(logpath=log_path)

        exit = False
        numIt = 0
        numIterationsTotal = 0
        while exit == False:
            print(numIterationsTotal)
            logger.info(str(numIterationsTotal))
            logger.info(str(time.asctime( time.localtime(time.time()) )))
            exit2 = False
            numIterationsInternas = 0
            
#             print('First')
            '''First Step: Optimizing class information of terms considering labeled documents'''
            while exit2 == False:
#                 print(numIt)
                
                estimatedClasses = self.classifyInstance(dataTrain)
                error = yTrain - estimatedClasses
                self.fbridge += self.errorCorrectionRate * np.dot(dataTrain.T,error)
                # print(np.sum(dataTrain.T))
                # print(np.sum(error))
                # print(np.dot(dataTrain.T,error))
                # print(self.fbridge[0])
                
                numIt += 1
                numIterationsInternas += 1
                
                # error: [numTrain,numClasses]
                error = pow(error,2)/2
                meanError = np.sum(error)/numTrain
                
                print('First Step meanError: ', meanError)
                logger.info('First Step meanError: '+ str(meanError))
                if self.maxNumberLocalIterations == numIterationsInternas or meanError < self.minError:
                    exit2 = True
            
#             print('Second')
            '''Second Step: Propagating class information from terms to unlabeled documents'''
             #基于term，将labeled的document的label传递给unlabeled的document

            fTestTemp = self.classifyInstance(dataTest)
            error = self.fTest - fTestTemp
            self.fbridge += self.errorCorrectionRate * np.dot(dataTest.T,error)
            # acmDif = np.sum(abs(self.fTest - fTestTemp))
            self.fTest = copy.copy(fTestTemp)
            # print('fTest: ',self.fTest[:5])

            
#             print('Third')
            '''Third Step: Optimizing class information of terms considering the class information assigned to unlabeled documents'''
            exit2 = False
            numIterationsInternas = 0
            while exit2 == False:
#                 print(numIt)
                
                # 增加鲁棒性？因为不可能只有train在影响啊
                estimatedClasses = self.classifyInstance(dataTest)
                # print('estimatedClasses: ',estimatedClasses[:5])
                error = self.fTest - estimatedClasses
                self.fbridge += self.errorCorrectionRate * np.dot(dataTest.T,error)
                
                numIt += 1
                numIterationsInternas += 1
                
                # error: [numTrain,numClasses]
                error = pow(error,2)/2
                meanError = np.sum(error)/numTrain
                
                print('Third Step meanError: ', meanError)
                logger.info('Third Step meanError: '+ str(meanError))
                if self.maxNumberLocalIterations == numIterationsInternas or meanError < self.minError: 
                    exit2 = True
                
            numIterationsTotal += 1
            numIt += 1
            if self.maxNumberGlobalIterations == numIterationsTotal:
                exit = True
    
        self.numIterations = numIt
        
        '''Assingning labels to unlabaled documents'''
        self.fTest = self.classifyInstance(dataTest)
        
        ypredict = []
        for i in self.fTest:
            if i[0] >= i[1]:
                ypredict.append(0)
            else:
                ypredict.append(1)
        # logger.info(str(self.fTest))
        
        ypredict = np.array(ypredict)
        return ypredict



input_path_aspect = '../raw_data/restaurants_aspect.csv'
input_path_sentiment = '../raw_data/restaurants_sentiment.csv'

aspect = pd.read_csv(input_path_aspect)
# sentiment = pd.read_csv(input_path_sentiment)

dataTrain = aspect.iloc[:3000,:-1]
dataTest = aspect.iloc[3000:,:-1]
yTrain_o = aspect.iloc[:3000,-1:]
yTest_o = aspect.iloc[3000:,-1:]

dataTrain = np.array(dataTrain)
dataTest = np.array(dataTest)
yTrain_o = np.array(yTrain_o)
yTest_o = np.array(yTest_o)


yTrain = []
for i in yTrain_o:
    if i == 'NO':
        yTrain.append([0,1])
    else:
        yTrain.append([1,0])
yTrain = np.array(yTrain)

yTest = []
for i in yTest_o:
    if i == 'NO':
        yTest.append([0,1])
    else:
        yTest.append([1,0])
yTest = np.array(yTest)



numTrain = dataTrain.shape[0]
numTest = dataTest.shape[0]
numTerms = dataTrain.shape[1]
numClasses = yTrain.shape[1]


dataTrain = normalize(dataTrain)
dataTest = normalize(dataTest)


model = TCHN(maxNumberGlobalIterations=3,maxNumberLocalIterations=100)
ypredict = model.train()

ylabel = yTest[:,0].astype(int)
ypredict = ypredict.astype(int)






precision, recall,  acc, f1_score, auc, matrix = helper_model.calculate('',ylabel,ypredict)


log_path = "logs/outcome.log"
if not os.path.exists("logs/"):
    utils.makedirs("logs/")
logger = helper_model.get_logger(logpath=log_path)

logger.info('f1_score: '+ str(f1_score))
logger.info('auc: '+ str(auc))