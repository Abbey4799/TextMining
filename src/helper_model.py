import random
import csv
import os
import pickle
import numpy as np
import pandas as pd
import datetime
import copy
import logging
from sklearn import metrics
from sklearn import model_selection

# all model can use


def calculate(name, labels, predictions):
    predictions = [1 if x >= 0.5 else 0 for x in predictions]

    precision = metrics.precision_score(labels, predictions)
    recall = metrics.recall_score(labels, predictions)
    f1_score = metrics.f1_score(labels, predictions)
    auc = metrics.roc_auc_score(labels, predictions)
    acc = metrics.accuracy_score(labels, predictions)
    confusion_matrix = metrics.confusion_matrix(labels, predictions)

    print('%s\nprecision\trecall\tacc\tf1_score\tauc' % (name))
    print('%.3f & %.3f & %.3f & %.3f & %.3f\n\n\n' %
          (precision, recall, acc, f1_score, auc))

    return precision, recall, acc, f1_score, auc, confusion_matrix



def get_logger(logpath, package_files=[],
			   displaying=True, saving=True, debug=False):
	logger = logging.getLogger()
	if debug:
		level = logging.DEBUG
	else:
		level = logging.INFO
	logger.setLevel(level)
	if saving:
		info_file_handler = logging.FileHandler(logpath, mode='w')
		info_file_handler.setLevel(level)
		logger.addHandler(info_file_handler)
	if displaying:
		console_handler = logging.StreamHandler()
		console_handler.setLevel(level)
		logger.addHandler(console_handler)

	for f in package_files:
		logger.info(f)
		with open(f, 'r') as package_f:
			logger.info(package_f.read())

	return logger