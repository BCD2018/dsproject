#coding: utf-8


import pandas as pd
from collections import Counter


'''

These code is for question 1,
i.e. Extract different statistic from the data.

Statistic we need:
    1.  number of sells
    2.  number of buys
    



'''

path = '/shared/mlrdir1/disk1/home/zixuan/PycharmProjects/ds_project/networktenxpayTX'

all_tokens = pd.read_csv(path,sep=' ',encoding='utf-8',header=0)

# buyer_id = [x for x in all_tokens['toNodeID']]
#
# buyer_id_dict = Counter(buyer_id)
#
# buyer_id_count = [value for key, value in buyer_id_dict.iteritems()] #extract the count
#
# print Counter(buyer_id_count)
#
# with open('buyer_count','w') as data:
#     data.writelines('number_of_buys' + '\t' + 'number_of_users' + '\n')
#     for key, value in Counter(buyer_id_count).iteritems():
#         data.writelines(str(key) + '\t' + str(value) + '\n')


seller_id = [x for x in all_tokens['fromNodeID']]

seller_id_dict = Counter(seller_id)

seller_id_count = [value for key, value in seller_id_dict.iteritems()] #取出统计数量

print Counter(seller_id_count)

with open('seller_count','w') as data:
    data.writelines('number_of_sells' + '\t' + 'number_of_users' + '\n')
    for key, value in Counter(seller_id_count).iteritems():
        data.writelines(str(key) + '\t' + str(value) + '\n')


