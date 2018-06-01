# -*- coding:utf-8 -*-
# python for data analysis  2.3 babynames data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# names1880 = pd.read_csv('C:/Users/dell/Desktop/pydata/datasets/babynames/yob1880.txt', names=['name', 'sex', 'births'])
years = range(1880, 2011)
pieces = []
columns = ['name', 'sex', 'births']
for year in years:
    path = 'C:/Users/dell/Desktop/pydata/datasets/babynames/yob%d.txt' % year
    frame = pd.read_csv(path, names=columns)
    frame['year'] = year
    pieces.append(frame)

names = pd.concat(pieces, ignore_index=True)
# total_births = names.pivot_table('births', index='year',
#                                  columns='sex', aggfunc=sum)
# total_births.plot(title='Total births by year and sex')


def add_prop(group):
    # 整数除法回向下取整
    births = group.births.astype(float)
    group['prop'] = births / births.sum()
    return group

names = names.groupby(['year', 'sex']).apply(add_prop)
# 检验分组prop总和是否为1
#print np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)
def get_top1000(group):
    return group.sort_index(by='births', ascending=False)[:1000]

grouped = names.groupby(['year', 'sex'])
top1000 = grouped.apply(get_top1000)
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']
total_births = top1000.pivot_table('births', index='year', columns='name',
                                    aggfunc=sum)
subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
# subset.plot(subplots=True, figsize=(12, 10), grid=False,
#             title='Number of births per year')
table = top1000.pivot_table('prop', index='year',
                            columns='sex', aggfunc=sum)
# table.plot(title='Sum of table1000.prop by year and sex',
#            yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10))
# plt.show()


def get_quantile_count(group, q=0.5):
    group = group.sort_index(by='prop', ascending=False)
    return group.prop.cumsum().searchsorted(q)[0] + 1  # searchsorted返回ndarray类型，取其数值

diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')
# diversity.plot(title='Number of popular names in top 50%')

# 从name列取出最后一个字母
get_last_letter = lambda x: x[-1]
last_letters = names.name.map(get_last_letter)
last_letters.name = 'last_letter'
new_table = names.pivot_table('births', index=last_letters,
                          columns=['sex', 'year'], aggfunc=sum)
subtable = new_table.reindex(columns=[1910, 1960, 2010], level='year')
letter_prop = subtable / subtable.sum().astype(float)
# fig, axes = plt.subplots(2, 1, figsize=(10, 10))
# letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
# letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female', legend=False)  # legend调整图例
# 图像设置（如间隔）在显示界面中可调
# plt.show()
dny_ts = letter_prop.ix[['d', 'n', 'y'], 'M'].T

all_names = top1000.name.unique()
mask = np.array(['lesl' in x.lower() for x in all_names])
lesley_like = all_names[mask]
filtered = top1000[top1000.name.isin(lesley_like)]
# print filtered.groupby('name').births.sum()
last_table = filtered.pivot_table('births', index='year',
                                  columns='sex', aggfunc='sum')
last_table = last_table.div(last_table.sum(1), axis=0)
last_table.plot(style={'M': 'k-', 'F': 'k--'})
plt.show()

