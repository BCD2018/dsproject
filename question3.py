#coding: utf-8


import pandas as pd
from collections import Counter
import time
from datetime import datetime
import numpy as np
from scipy.stats.stats import pearsonr
from sklearn.linear_model import LinearRegression

'''

This code is for question 3,
i.e. Design three features and train a multi regression model

price: (Pt - P(t-1))/Pt-1

sklearn is used to do the multiple regression

'''

maximum_amount = pow(10,21)

path = '/shared/mlrdir1/disk1/home/zixuan/PycharmProjects/ds_project/networktenxpayTX'
price_path = '/shared/mlrdir1/disk1/home/zixuan/PycharmProjects/ds_project/tenxpay'

# path = '/shared/mlrdir1/disk1/home/zixuan/PycharmProjects/ds_project/networkzrxTX'
# price_path = '/shared/mlrdir1/disk1/home/zixuan/PycharmProjects/ds_project/zrx'


all_tokens = pd.read_csv(path,sep=' ',encoding='utf-8',header=0)


# read transaction time
transaction_time = [
    str(datetime.utcfromtimestamp(float(x)).strftime('%m/%d/%Y')) for x in all_tokens['unixTime']]
transaction_amount = [int(x) for x in all_tokens['tokenAmount']]
transaction_buyer = [int(x) for x in all_tokens['toNodeID']]






# print transaction_time

# read transaction_amount
tokens_price = [str(x) for x in pd.read_csv(price_path,sep='\t',encoding='utf-8',header=0)['Low']]
tokens_date = [str(x) for x in pd.read_csv(price_path,sep='\t',encoding='utf-8',header=0)['Date']]

# print tokens_price
# print tokens_date

# bin into different histogram
bin_n = 20

# print transaction_amount[0]
# print [ x_id*maximum_amount/bin_n for x_id in range(bin_n)][-1]
#
# print [ x_id*maximum_amount/bin_n for x_id in range(bin_n)]
layers =  np.digitize(transaction_amount, bins=[ int(x_id*maximum_amount/bin_n) for x_id in range(bin_n)])

# print tokens_price
# operate on each layer:
print Counter(layers)
print len(layers)
print len(transaction_time)
print len(tokens_price)
print len(tokens_date)
import math

tokens_date = [str('0'+x) if len(x.split('/')[0])==1 else x for x in tokens_date ]

# print tokens_date
print layers[transaction_time.index('03/14/2018')]
print transaction_time.index('05/01/2018')
print tokens_date.index('05/01/2018')
print tokens_date
# layers = [layers[43819]]
# print transaction_time

p_save = [] #pearson value save
number_save = []
price_save = []
r_squre_save = []
prediction_save = []



for layer_no in range(bin_n+1):

    print 'layer_no: ' + str(layer_no)
    if layer_no == 0: continue
    layer_date_price = {}
    for data_id,layer_id in enumerate(layers):
        # print layer_id
        if layer_id == layer_no:

            if transaction_time[data_id] in layer_date_price:
                # already there, #transaction simply + 1 #same date same low price
                layer_date_price[transaction_time[data_id]][1] = layer_date_price[transaction_time[data_id]][1] + 1

            else:   # not there, a new date
                if transaction_time[data_id] not in tokens_date: continue
                tokens_date_id = tokens_date.index(transaction_time[data_id])
                layer_date_price[transaction_time[data_id]] = [tokens_price[tokens_date_id],1]

    # print layer_date_price

    number_of_transaction = [float(value[1]) for key, value in layer_date_price.iteritems()]
    y = [float(value[0]) for key, value in layer_date_price.iteritems()]


    p = pearsonr(number_of_transaction,y)

    sqrt_number_of_transaction = [math.sqrt(x) for x in number_of_transaction]
    sq_number_of_transaction = [x*x for x in number_of_transaction]

    number_of_transaction = np.array(number_of_transaction).reshape(-1,1)
    sqrt_number_of_transaction = np.array(sqrt_number_of_transaction).reshape(-1,1)
    sq_number_of_transaction = np.array(sq_number_of_transaction).reshape(-1,1)


    features = np.hstack((number_of_transaction,sqrt_number_of_transaction,sq_number_of_transaction))
    print features[0].shape
    reg = LinearRegression().fit(features, y)
    print reg.score(features, y)
    print p[0]

    prediction = [reg.predict(np.array(features[x_id]).reshape(1,-1))[0] for x_id,x in enumerate(features)]

    prediction_save.append(prediction)
    p_save.append(p[0])
    number_save.append(number_of_transaction)
    price_save.append(y)
    r_squre_save.append(reg.score(features, y))


with open('prediction','w') as prediction_file:

    layer_id = r_squre_save.index(max(r_squre_save))
    for x_id,x in enumerate(prediction_save[layer_id]):
        prediction_file.writelines(str(prediction_save[layer_id][x_id]) + '\t' + str(price_save[layer_id][x_id]) + '\n')




with open('pearson_vs_r_squre','w') as multi_regression_file:
    for x_id,x in enumerate(p_save):
        multi_regression_file.writelines(str(p_save[x_id]) + '\t' + str(r_squre_save[x_id]) + '\n')