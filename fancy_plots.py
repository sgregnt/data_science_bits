import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from df_aux import df_group_accupancy_by_column, running_mean

def plot_target_col_by_group_compare(dfs, dfs_names, groupby,
                                     add_scatter=[True],
                                     target_col='dim_is_requested'):
    """Aggregate data by features and plot running average of target_col
    combine different cities on the same plot"""

    for col, scatter in zip(groupby, add_scatter):

        fig = plt.figure()
        ax = fig.add_subplot(111)

        for df, name, c in zip(dfs, dfs_names, ['r', 'g', 'b']):

            # Wrapper to aggregate statistics of target_col
            # for groups defined by col
            x, z = df_group_accupancy_by_column(df, col, np.mean, target_col)

            if scatter:
                ax.scatter(x, z, c= c, s=5, alpha=0.3, label='_nolegend_')
            else:
                plt.plot(x, z, c + '-', linewidth=2, label=name)

            # compute running mean if sequence is long enough
            n = int(len(z) * 0.1)
            if n > 5:
                z_avg = running_mean(list(z), n)
                plt.plot(list(x[(n - 1) // 2:-(n - 1) // 2]),
                         z_avg,
                         c + '-',
                         linewidth=2,
                         label=name)

        plt.title("Mean(%s) vs %s" % (target_col, col))

        plt.legend()
        plt.xlabel(col)
        plt.ylabel('%s' % (target_col))
        plt.show()

def compare_histograms(dfs, dfs_names, colors, col_name, bins, upper=1000):
    """Given list of dfs with their corresponding names compares histogram
    of column "col_name" trunkated at value upper.
    """

    data = []
    for df, name in zip(dfs, dfs_names):
        x = df[col_name][df[col_name] < upper]
        data.append(x)

    plt.hist(data, alpha=1, color=colors, bins=bins, label=dfs_names, density=True)
    plt.legend(loc='upper right')
    plt.title('Distribution of %s' % (col_name))
    plt.show()
