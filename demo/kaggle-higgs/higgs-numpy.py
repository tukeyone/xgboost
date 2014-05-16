#!/usr/bin/python
# this is the example script to use xgboost to train 
import sys
import numpy as np
# add path of xgboost python module
sys.path.append('../../python/')
import xgboost as xgb

test_size = 550000

# path to where the data lies
dpath = 'data'

# load in training data, directly use numpy
dtrain = np.loadtxt( dpath+'/training.csv', delimiter=',', skiprows=1, converters={32: lambda x:int(x=='s') } )
label  = dtrain[:,32]
data   = dtrain[:,1:31]
# rescale weight to make it same as test set
weight = dtrain[:,31] * float(test_size) / len(label)

sum_wpos = sum( weight[i] for i in xrange(len(label)) if label[i] == 1.0  )
sum_wneg = sum( weight[i] for i in xrange(len(label)) if label[i] == 0.0  )

# print weight statistics 
print 'weight statistics: wpos=%g, wneg=%g, ratio=%g' % ( sum_wpos, sum_wneg, sum_wneg/sum_wpos )

# construct xgboost.DMatrix from numpy array, treat -999.0 as missing value
xtrain = xgb.DMatrix( data, label=label, missing = -999.0 )

# setup parameters for xgboost
params = {}
# use logistic regression loss
param['loss_type'] = 3
# scale weight of positive examples
param['scale_pos_weight'] = sum_wpos/sum_wpos
param['bst:eta'] = 0.1 
param['bst:max_depth'] = 6
param['eval_metric'] = 'ams@0.15'
param['silent'] = 1
param['eval_train'] = 1
param['nthread'] = 16

# boost 120 tres
num_round = 120
print 'loading data end, start to boost trees'
bst = xgb.train( xtrain, param, num_round );
# save out model
bst.save_model('higgs.model')

print 'finish training'