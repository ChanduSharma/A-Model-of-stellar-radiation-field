import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
import os
import math
import time

def ridge_regression_model(filename):

	df = pd.read_csv(filename)
	#df = (df - df.mean()) / (df.max() - df.min())
	columns = df.columns.tolist()
	columns = [c for c in columns if c != 'Flux']
	target = 'Flux'
	train = df.sample(frac = 0.8 , random_state = 1)
	test = df.loc[~df.index.isin(train.index)]
	model = Ridge(alpha = 0.5)
	y = model.fit(train[columns],train[target])
	predictions = model.predict(test[columns])
	print('Mean squarred error=',mean_squared_error(predictions,test[target]))



if __name__ == '__main__':
	ridge_regression_model('dataset_for_lr.csv')