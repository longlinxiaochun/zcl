# -*- coding:utf-8 -*-
# python for data analysis  8 use  data
import numpy as np
from pandas import DataFrame
import pandas as pd
import matplotlib.pyplot as plt

path = 'C:/Users/dell/Desktop/pydata/datasets/fec/P00000001-ALL.csv'
fec = pd.read_csv(path, low_memory=False)

# DtypeWarning: Columns (6) have mixed types. Specify dtype option on import or set low_memory=False.
# explain:
# Pandas can only determine what dtype a column should have once the whole file is read.
# This means nothing can really be parsed before the whole file is read
# unless you risk having to change the dtype of that column when you read the last value
# The reason you get this low_memory warning is because guessing dtypes for each column is very memory demanding.
# Pandas tries to determine what dtype to set by analyzing the data in each column.
unique_cands = fec.cand_nm.unique()  # 筛选候选人名单
# 添加政党信息
parties = {'Bachmann, Michelle': 'Republican',
           'Cain, Herman': 'Republican',
           'Gingrich, Newt': 'Republican',
           'Huntsman, Jon': 'Republican',
            'Johnson, Gary Earl': 'Republican',
            'McCotter, Thaddeus G': 'Republican',
           'Obama, Barack': 'Democrat',
           'Paul, Ron': 'Republican',
           'Pawlenty, Timothy': 'Republican',
           'Perry, Rick': 'Republican',
           "Roemer, Charles E. 'Buddy' III": 'Republican',
           'Romney, Mitt': 'Republican',
           'Santorum, Rick': 'Republican'}
fec['party'] = fec.cand_nm.map(parties)
fec['party'].value_counts()
# 发现存在负出资（退款），舍去
fec = fec[fec.contb_receipt_amt > 0]
fec_mrbo = fec[fec.cand_nm.isin(['Obama, Barack', 'Romney, Mitt'])]
# 将赞助职业分类,将一个职业信息映射到另一个
occ_mapping = {'INFORMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED',
               'INFORMATION REQUESTED': 'NOT PROVIDED',
               'INFORMATION REQUESTED (BEST EFFORTS)': 'NOT PROVIDED',
               'C.E.O.': 'CEO'}
f = lambda x: occ_mapping.get(x, x)
fec.contbr_occupation = fec.contbr_occupation.map(f)
emp_mapping = {'INFORMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED',
               'INFORMATION REQUESTED': 'NOT PROVIDED',
               'SELF': 'SELF-EMPLOYED',
               'SELF EMPLOYED': 'SELF-EMPLOYED'}
f = lambda x: emp_mapping.get(x, x)
fec.contbr_employer = fec.contbr_employer.map(f)
by_occupation = fec.pivot_table('contb_receipt_amt',
                                index='contbr_occupation',
                                columns='party', aggfunc='sum')
over_2mm = by_occupation[by_occupation.sum(1) > 2000000]
# over_2mm.plot(kind='barh')


def get_top_amounts(group, key, n=5):
    totals = group.groupby(key)['contb_receipt_amt'].sum()
    return totals.sort_values(ascending=False)[:n]
grouped = fec_mrbo.groupby('cand_nm')
# groupby技术是拆分对象特定轴，再对各分组进行运算后合并，返回是一个groupby对象，只能进行运算操作
grouped.apply(get_top_amounts, 'contbr_occupation', n=7)
grouped.apply(get_top_amounts, 'contbr_employer', n=10)

bins = np.array([0, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000])
labels = pd.cut(fec_mrbo.contb_receipt_amt, bins)
grouped_2 = fec_mrbo.groupby(['cand_nm', labels])
grouped_2.size().unstack(0)
bucket_sums = grouped_2.contb_receipt_amt.sum().unstack(0)  # 对出资额进行求和
normed_sums = bucket_sums.div(bucket_sums.sum(axis=1), axis=0)
normed_sums[:-2].plot(kind='barh', stacked=True)

# exercise:根据赞助人的姓名和邮编对数据聚合，找出哪些人多次小额捐款，哪些大额捐款
grouped_ex = fec_mrbo.groupby(['contbr_zip', 'contbr_nm']).size()
# contbr_nm与contbr_zip在labels下的整合数量不同,无法unstack
# size返回分组大小，聚合后统计的即为区间内次数
grouped_exsum = fec_mrbo.groupby(['contbr_zip', 'contbr_nm', labels]).contb_receipt_amt.sum()
grouped_few = grouped_ex[grouped_ex > 1]  # 多次捐款，还需筛选出小额的
grouped_much = grouped_exsum[grouped_exsum > 10000]

# 根据州统计赞助信息，并在地图上显示（未完成）
grouped_3 = fec_mrbo.groupby(['cand_nm', 'contbr_st'])
totals = grouped_3.contb_receipt_amt.sum().unstack(0).fillna(0)
totals = totals[totals.sum(1) > 100000]
percent = totals.div(totals.sum(1), axis=0)