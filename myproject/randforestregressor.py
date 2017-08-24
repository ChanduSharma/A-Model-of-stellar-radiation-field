import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import os
import math
import time



def random_forest_regression_model(filename):

	df = pd.read_csv(filename)
	#df = (df - df.mean()) / (df.max() - df.min())
	columns = df.columns.tolist()
	columns = [c for c in columns if c != 'Flux']
	target = 'Flux'
	train = df.sample(frac = 0.7 , random_state = 1)
	test = df.loc[~df.index.isin(train.index)]
	model = RandomForestRegressor(n_estimators=10, min_samples_leaf=50, n_jobs= -1, random_state=1)
	y = model.fit(train[columns],train[target])
	predictions = model.predict(test[columns])
	print('Mean squarred error=',mean_squared_error(predictions,test[target]))


if __name__ == '__main__':
	random_forest_regression_model('dataset_for_lr.csv')
