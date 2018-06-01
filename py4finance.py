# -*- coding:utf-8 -*-
import pandas as pd
import datetime as dt
from urllib import urlretrieve
import numpy as np
"""
# scatter plot
import matplotlib.pyplot as plt
y = np.random.standard_normal((1000, 2))
c = np.random.randint(0, 10, len(y))
plt.figure(figsize=(7, 5))
plt.scatter(y[:, 0], y[:, 1], c=c, marker='o')
plt.colorbar()
plt.grid(True)
plt.xlabel('1st')
plt.ylabel('2nd')
plt.title('scatter plot')
"""
# High-Frequency Data
import urllib2
proxy_info = {'host': 'web-proxy.oa.com', 'port': 8080}
proxy_support = urllib2.ProxyHandler({"http": "http://%(host)s:%(port)d" % proxy_info})
opener = urllib2.build_opener(proxy_support)
urllib2.install_opener(opener)
url1 = 'http://hopey.netfonds.no/posdump.php? '
url2 = 'date=%s%s%s&paper=AAPL.O&csv_format=csv'
url = url1 + url2
year = '2014'
month = '09'
days = ['22', '23', '24', '25']
AAPL = pd.DataFrame()
for day in days:
    AAPL = AAPL.append(pd.read_csv(url % (year, month, day),
                                   index_col=0, header=0, parse_dates=True))
AAPL.columns = ['bid', 'bdepth', 'bedtht', 'offer', 'odepth', 'odeptht']
AAPL.info



