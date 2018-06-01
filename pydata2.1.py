# -*- coding:utf-8 -*-
# python for data analysis  4 numpy ndrray
import numpy as np
arr = np.arange(9)
arr_slice = arr[4:7]
arr_slice[1] = 123
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
arr2d[:2]
arr2d[:2, 1:]
arr2d[:, :2]
a = np.array([1, 2, 3])
print a ** 2
arr = np.random.randn(4, 4)
print np.where(arr > 0, 2, -2)  # where(judge, if ,else)

# example: random walk
nwalks = 5000
nsteps = 1000
draws = np.random.randint(0, 2, size=(nwalks, nsteps))  # 列行
steps = np.where(draws > 0, 1, -1)
walks = steps.cumsum(1)
walks.max()
walks.min()
hits30 = (np.abs(walks) >= 30).any(1)  # 转换为bool型,存在大于三十则为真
crossing_times = (np.abs(walks[hits30]) >= 30).argmax(1)
print len(hits30)
