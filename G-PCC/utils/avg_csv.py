import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def average_csv(csvs):
    input_pds = [pd.read_csv(x) for x in csvs]

    rates = len(input_pds[1].index)
    metrics = input_pds[1].columns
    print(rates, metrics)

    for rate in range(rates):
        # print(rate)
        results = {}
        for i, metric in enumerate(metrics):
            results[metric] = []
            for j, input_pd in enumerate(input_pds):
                results[metric].append(input_pd[metric][rate])
            # mean
            results[metric] = np.mean(results[metric])

        results = pd.DataFrame([results])
        if rate == 0:
            all_results = results.copy(deep=True)
        else:
            all_results = pd.concat((all_results, results), ignore_index=True)
            
    return all_results


def plot_panda_csv(df, x_axis, y_axis, label, xlabel, ylabel, dest_file):
    name = dest_file.split('/')[-1].split('.')[0]
    fig, ax = plt.subplots(figsize=(7, 4))
    plt.plot(np.array(df[x_axis][:]), np.array(df[y_axis][:]), label=label, marker='x', color='red')
    plt.title(name)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(ls='-.')
    plt.legend(loc='lower right')
    fig.savefig(dest_file, dpi=300)
    
    return