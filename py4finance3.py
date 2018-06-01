# -*- coding:utf-8 -*-
# principal component analysis
import numpy as np
import pandas as pd
import pandas_datareader as web
from sklearn.decomposition import KernelPCA
import matplotlib.pyplot as plt
symbols = ['ADS.DE', 'ALV.DE', 'BAS.DE', 'BAYN.DE', 'BEI.DE',
           'BMW.DE', 'CBK.DE', 'CON.DE', 'DAI.DE', 'DB1.DE',
           'DBK.DE', 'DPW.DE', 'DTE.DE', 'EOAN.DE', 'FME.DE',
           'FRE.DE', 'HEI.DE', 'HEN3.DE', 'IFX.DE', 'LHA.DE',
           'LIN.DE', 'LXS.DE', 'MRK.DE', 'MUV2.DE', 'RWE.DE',
           'SAP.DE', 'SDF.DE', 'SIE.DE', 'TKA.DE', 'VOW3.DE',
           '^GDAXI']
data = pd.DataFrame()
for sym in symbols:
    data[sym] = web.get_data_yahoo(sym)['Close']
data = data.dropna()
dax = pd.DataFrame(data.pop('^GDAXI'))
scale_function = lambda x: (x - x.mean()) / x.std()
pca = KernelPCA().fit(data.apply(scale_function))
get_we = lambda x: x / x.sum()
pca = KernelPCA(n_components=1).fit(data.apply(scale_function))
dax['PCA_1'] = pca.transform(-data)
dax.apply(scale_function).plot(figsize=(8, 4))

# 5个主成分
pca = KernelPCA(n_components=5).fit(data.apply(scale_function))
pca_components = pca.transform(-data)
weights = get_we(pca.lambdas_)
dax['PCA_5'] = np.dot(pca_components, weights)
dax.apply(scale_function).plot(figsize=(8, 4))


