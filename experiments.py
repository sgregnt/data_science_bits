import pandas as pd
import numpy as np

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
