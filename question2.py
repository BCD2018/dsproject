#coding: utf-8


import pandas as pd
from collections import Counter
import time
from datetime import datetime
import numpy as np
from scipy.stats.stats import pearsonr


'''

This code is for question 2,
i.e. Design layer and compute the correlation between the layer feature and the price

Some concepts:
    1.  Layer: split the data into different bins
    2.  feature of layers: number of transaction (Thus it limits the size of data in each layer)
    3.  token price (Y-axis) ('xpa')
    4.  Date (X-axis)
    



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
tokens_date = [str('0'+x) if len(x.split('/')[0])==1 else x for x in tokens_date ]


# print tokens_date
print layers[transaction_time.index('03/14/2018')]
print transaction_time.index('05/01/2018')
print tokens_date.index('05/01/2018')
print tokens_date
# layers = [layers[43819]]
# print transaction_time

p_save = []
number_save = []
price_save = []


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


    x = [float(value[1]) for key, value in layer_date_price.iteritems()]
    y = [float(value[0]) for key, value in layer_date_price.iteritems()]
    p = pearsonr(x,y)
    p_save.append(p[0])

    number_save.append(x)
    price_save.append(y)

    print x
    print y
    print p

    # break
print max(p_save)
print min(p_save)

for x_id,x in enumerate(number_save[p_save.index(max(p_save))]):
    print str(1.0*x/100)+'\t'+str(price_save[p_save.index(max(p_save))][x_id])

    #
    # print layer_date
    # print layer_price
    #
    # with open('layer_no_'+str(layer_no),'w') as data:
    #     data.writelines('date' + '\t' + 'price' + '\n')
    #     for x_id,x in enumerate(layer_date):
    #         data.writelines(str(layer_date[x_id]) + '\t' + str(layer_price[x_id]) + '\n')

    # break
    # How come all in the same date???


