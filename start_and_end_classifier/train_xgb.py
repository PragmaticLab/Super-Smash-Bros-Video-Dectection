import logging 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import sys
sys.path.append("../utils/")
from dataset_construction_util import generate_basic_image_dataset
import os
import numpy as np 
import xgboost as xgb 
from sklearn.cross_validation import train_test_split


X, y, file_list = generate_basic_image_dataset("../dataset_generated/posDir/", "../dataset_generated/negDir/", sampleMultiplier=2.5) 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)
logging.info("Loaded dataset! train shape: %s, test shape: %s" % (str(X_train.shape), str(X_test.shape)))


param = {'bst:max_depth':4, 'bst:eta':0.05, 'objective':'binary:logistic', 'nthread':-1, 'eval_metric': ['error', 'auc']}
param['min_child_weight'] = 1.41
param['colsample_bytree'] = 0.3
evallist  = [(dtest,'eval'), (dtrain,'train')]


num_round = 50
bst = xgb.train(param, dtrain, num_round, evallist, early_stopping_rounds=5)
bst.save_model("models/curr_model")

# just testing now:
dval = xgb.DMatrix(X)
y_hat = bst.predict(dval)
print "\n\nWe got these files wrong:"
for i, (y, y_h) in enumerate(zip(y, y_hat)):
	if y != round(y_h):
		print file_list[i]
