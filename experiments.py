import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from fancy_plots import compare_histograms, plot_target_col_by_group_compare
#=========================================
# Index in data frame that is not integer
#=========================================

data = pd.Series([0.25, 0.5, 0.75, 1.0], index=['a', 'b', 'c', 'd'])
print("data.values", data.values)
print("data.index", data.index)
print("data['a']", data['a'])

data = pd.Series([0.25, 0.5, 0.75, 1.0])
print("data.values", data.values)
print("data.index", data.index)
print("data[0]", data[0])

#=========================================
# Groupby key, then run calculation on each of the
# groups and show histogram colored by groups
#=========================================

rng = np.random.RandomState(0)
df = pd.DataFrame({'key': ['A', 'B', 'C', 'A', 'B', 'C'],
                    'data1': range(6),
                    'data2': rng.randint(0, 10, 6)},
                    columns = ['key', 'data1', 'data2'])
print(df)
res = df.groupby('key')
print(res)

res = df.groupby('key').aggregate(['min', np.median, max])
print(res)

# does not show that the function computed on data1 and data2 are different
res = df.groupby('key').aggregate({'data1': 'min', 'data2': 'max'}).plot.bar(rot=0)
plt.show()

# produces histogram with bars colored according to key
res = df.groupby('key')['data1'].min().plot.bar(rot=0)
plt.title("my title")
plt.show()

# produces histogram with bars of the same color
res = df.groupby('key').aggregate({'data1': 'min'}).plot.bar(rot=0)
plt.title("my title")
plt.show()

# produces histogram with bars colored according to key
res = df.groupby('key').aggregate({'data1': 'min'}).squeeze().plot.bar(rot=0)
plt.title("my title")
plt.show()

#=========================================
# compare histogrmas
#=========================================

n = 100
val1 = np.sin((np.array(range(n))/(n*1.0)) * np.pi) + np.random.rand(n) * 0.05
val2 = np.cos((np.array(range(n))/(n*1.0)) * np.pi) + np.random.rand(n) * 0.05
df1 = pd.DataFrame({'val': val1})
df2 = pd.DataFrame({'val': val2})

dfs = [df1, df2]
dfs_names = ['sin', 'cos']

compare_histograms(dfs=dfs, dfs_names=dfs_names,
                   col_name='val',
                   bins=25, colors=['r', 'c'])

#=========================================
# compare running average
#=========================================

n = 10000
val1 = np.sin((np.array(range(n))/(n*1.0)) * np.pi) + np.random.rand(n) * 0.05
val2 = np.cos((np.array(range(n))/(n*1.0)) * np.pi) + np.random.rand(n) * 0.05

cham_cham1 = np.random.rand(n) * 0.05
cham_cham2 = np.random.rand(n) * 0.05

k = 100

key1 = np.array(range(n)) % k
key2 = np.array(range(n)) % k

rand_key1 = (np.random.rand(n) * k).astype(int)
rand_key2 = (np.random.rand(n) * k).astype(int)

df1 = pd.DataFrame({'val': val1, 'cham_cham' : cham_cham1, 'key' : key1, 'rand_key' : rand_key1})
df2 = pd.DataFrame({'val': val2, 'cham_cham' : cham_cham2, 'key' : key2, 'rand_key' : rand_key2})

dfs = [df1, df2]
dfs_names = ['sin', 'cos']

plot_target_col_by_group_compare(dfs=dfs, dfs_names=dfs_names,
                                 groupby=['key', 'rand_key'],
                                 add_scatter=[True] * len(['key', 'rand_key']),
                                 target_col='val')

