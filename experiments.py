import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from fancy_plots import compare_histograms, plot_target_col_by_group_compare

index = 1

def header():
    """Separator of different code sinppets"""

    global index
    print('*' * 50)
    print('*** (' + str(index) + ')')
    print('*' * 50)
    index = index + 1

def caption(string):
    """Wrappert to print out captions"""

    print('*** (' + string + ') ')

if __name__ == '__main__':

    #=========================================
    # Index in data frame that is not integer
    #=========================================

    header()

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

    header()

    rng = np.random.RandomState(0)
    df = pd.DataFrame({'key': ['A', 'B', 'C', 'A', 'B', 'C'],
                        'data1': range(6),
                        'data2': rng.randint(0, 10, 6)},
                        columns = ['key', 'data1', 'data2'])

    caption("data frame")
    print(df)
    res = df.groupby('key')
    caption("group by key")
    print(res)

    res = df.groupby('key').aggregate(['min', np.median, max])
    caption("group by key aggregate minimum")
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

    header()

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

    header()

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

    #=========================================
    # categoriacal variables groupby,
    # checks all combinations
    # when one of the variables is categorical
    #=========================================

    header()

    df = pd.DataFrame({'col1': ['x', 'x', 'y'], 'col2': [0, 1, 0], 'col3': [7, 8, 9]})

    caption('df')
    print(df)
    print("type(df['col1'][0])", type(df['col1'][0]))
    caption('df group by col1 and col2')
    print(df.groupby(['col1', 'col2']).mean())


    df['col1'] = df['col1'].astype('category')
    caption('df with categorial col1')
    print(df)
    print("type(df['col1'][0])", type(df['col1'][0]))
    caption('df group by col1 and col2 with categorical col1')
    print(df.groupby(['col1', 'col2']).mean())

    #=========================================
    # rotated labels at barplots
    # example from https://stackoverflow.com/questions/32244019/how-to-rotate-x-axis-tick-labels-in-pandas-barplot
    #=========================================

    header()

    df = pd.DataFrame({ 'celltype' : ["foo", "bar", "qux", "woz"],
                        's1' : [5, 9, 1, 7], 's2' : [12, 90, 13, 87]})
    caption('df')
    print(df)
    df.set_index(["celltype"], inplace = True)
    df.plot(kind='bar', alpha=0.75)
    plt.show()

    #=========================================
    # Barplots for two categories stacked and unstacked
    #=========================================

    header()

    df = pd.DataFrame({'celltype' : ["foo", "bar", "qux", "woz"],
                        's1' : [5, 7, 5, 7], 's2' : [12, 90, 13, 87]})

    caption("stacked index")
    print(df.groupby(['celltype', 's1']).mean())

    # columns will be funky with two level names (multi-index columns)
    caption("unstacked index 1")
    df_grouped = df.groupby(['celltype', 's1']).mean().unstack()
    print(df_grouped)

    # same as the previous unstack but with columns and rows switched
    caption("unstacked index 0")
    df_grouped = df.groupby(['celltype', 's1']).mean().unstack(0)
    print(df_grouped)

    #=========================================
    # fixing columns multiindex issue
    # checkout https://www.youtube.com/watch?v=kJsiiPK5sxs
    #=========================================

    header()

    caption("df_grouped.columns")
    print(df_grouped.columns)
    # output -> df_grouped.columns MultiIndex(levels=[['s2'], ['bar', 'foo', 'qux', 'woz']],
    #                                         labels=[[0, 0, 0, 0], [0, 1, 2, 3]],
    #                                         names=[None, 'celltype'])

    caption("df_grouped.columns.values")
    print(df_grouped.columns.values)
    # output -> df_grouped.columns.values [('s2', 'bar') ('s2', 'foo') ('s2', 'qux') ('s2', 'woz')]

    df_grouped.columns = ['__'.join(col_name).strip() for col_name in df_grouped.columns.values]
    caption('df_grouped.columns')
    print(df_grouped.columns)

    caption("df_grouped fixed")
    print(df_grouped)

    #=========================================
    # Pivottable
    # example from https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.pivot_table.html
    #=========================================

    header()

    df = pd.DataFrame({"A": ["foo", "foo", "foo", "foo", "foo",
                             "bar", "bar", "bar", "bar"],
                       "B": ["one", "one", "one", "two", "two",
                             "one", "one", "two", "two"],
                       "C": ["small", "large", "large", "small",
                             "small", "large", "small", "small",
                             "large"],
                       "D": [1, 2, 2, 3, 3, 4, 5, 6, 7],
                       "E": [2, 4, 5, 5, 6, 6, 8, 9, 9],
                       "F": ["l", "l", "s", "s",
                             "s", "l", "s", "s",
                             "l"] })

    # show results of sum over column 'D' as a confusion table
    # with values index crossed by 'C' and 'F' with missing values filled by 0s
    table_a = pd.pivot_table(df, values='D', index=['A', 'B'], columns=['C', 'F'], aggfunc=np.sum, fill_value=0)
    caption('pivot table_a')
    print(table_a)

    table_b = pd.pivot_table(df, values='D', index=['A', 'B'], columns=['C'], aggfunc=np.sum, fill_value=0)
    caption('pivot table_b')
    print(table_b)

    # =========================================
    # One hot encoding
    # =========================================

    header()

    caption("get dummies trial")
    print(pd.get_dummies(df, columns=['A']))