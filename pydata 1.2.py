# -*- coding:utf-8 -*-
# python for data analysis  2.2 movielens 1m data
from pandas import DataFrame, Series
import pandas as pd
unames = ['user_id', 'gender', 'age','occupation', 'zip']
users = pd.read_table('C:/Users/dell/Desktop/pydata/datasets/movielens/users.dat',
                      sep='::', header=None, names=unames, engine='python')
rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('C:/Users/dell/Desktop/pydata/datasets/movielens/ratings.dat',
                        sep='::', header=None, names=rnames, engine='python')
mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('C:/Users/dell/Desktop/pydata/datasets/movielens/movies.dat',
                       sep='::', header=None, names=mnames, engine='python')
data = pd.merge(pd.merge(ratings, users), movies)
mean_ratings = data.pivot_table('rating', index='title',
                                columns='gender', aggfunc='mean')  # 做透视表，相当于excel上工作
# 按title对title进行分类，对应为数字的列会自动求和，而为字符串类型的列则不显示
ratings_by_title = data.groupby('title').size()  # size()可以对各个title下数目进行计数
# print ratings_by_title[:5]
active_titles = ratings_by_title.index[ratings_by_title >= 250]
mean_ratings = mean_ratings.ix[active_titles]  # ix通过行标签或行号索引
top_female_ratings = mean_ratings.sort_index(by='F', ascending=False)
mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sroted_by_diff = mean_ratings.sort_index(by='diff')

