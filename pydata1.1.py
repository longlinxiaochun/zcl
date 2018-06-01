# -*- coding:utf-8 -*-
# python for data analysis  2.1 use.gov data
import json
from pandas import DataFrame, Series
import numpy as np
import matplotlib.pyplot as plt
path = 'C:/Users/dell/Desktop/pydata/datasets/bitly_usagov/example.txt'
open(path).readline()
records = [json.loads(line) for line in open(path)]
#  print records[0]['tz']
#  time_zones = [rec['tz'] for rec in records if 'tz' in rec]
#  print time_zones[:10]
frame = DataFrame(records)
#  print frame['tz'][:10]
tz_counts = frame['tz'].value_counts()
# print tz_counts[:10]
clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unkonw'
tz_counts = clean_tz.value_counts()
#  print tz_counts[:10]
# tz_counts[:10].plot(kind='barh', rot=0)
# 导入matplotlib才能显示图像
# plt.show()
results = Series([x.split()[0] for x in frame.a.dropna()])
# print results.value_counts()[:5]
cframe = frame[frame.a.notnull()]
operating_system = np.where(cframe['a'].str.contains('Windows'),
                            'Windows', 'Not Windows')
# print operating_system[:5]
by_tz_os = cframe.groupby(['tz', operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)  # unstack分栈处理
# print agg_counts[:10]
indexer = agg_counts.sum(1).argsort()  # sum(1)每行数据相加 argsort输出排序数
count_subset = agg_counts.take(indexer)[-10:]
# print count_subset[-10:]
# count_subset.plot(kind='barh', stacked=True)
# plt.show()
normed_subset = count_subset.div(count_subset.sum(1), axis=0)  # 矩阵除法
normed_subset.plot(kind='barh', stacked=True)
plt.show()
