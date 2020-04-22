import matplotlib.pyplot as plt
import numpy as np
import os
import json
import seaborn as sns
import re

sns.set(style="darkgrid")

gcc_9_key = "4*4*4*4*4*4*4*4*4*4*((d * (1 - d))*(c * (1 - c))*(J * (1 - J))*(N * (1 - N))*(M * (1 - M))*(a * (1 - a))*(Y * (1 - Y))*(k * (1 - k))*(x * (1 - x))*(g * (1 - g)))"
gcc_49_key = "4*4*4*4*4*4*4*4*4*4*((X * (1 - X))*(l * (1 - l))*(b * (1 - b))*(K * (1 - K))*(v * (1 - v))*(Q * (1 - Q))*(J * (1 - J))*(o * (1 - o))*(r * (1 - r))*(L * (1 - L)))"
num_params = [10, 2010, 4010, 6010, 8010, 10010, 20010, 30010, 40010, 50010, 60010, 70010, 80010, 90010 ]
def atoi(text):
    return int(text) if text.isdigit() else text
def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def convert_files_to_lists(file_location, key=""):
    wenzel_static_times = []
    wenzel_dynamic_times = []
    with open(file_location) as json_data:
        data = json.load(json_data)
        runs = data[key]
        for num_param in num_params:
            wenzel_static_times.append(runs[str(num_param)]['wenzel_static'])
            wenzel_dynamic_times.append(runs[str(num_param)]['wenzel_dynamic'])
    return wenzel_static_times, wenzel_dynamic_times

def generate_two_graph(avg_one, avg_two, denom, suffix="", ylabel="Time (s)"):
    fig = plt.figure(figsize=(20, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(denom, avg_one, color='#1abc9c', linestyle='dashed',  markersize=7)
    ax.plot(denom, avg_two, color='#f1c40f', linestyle='dashed', markersize=7)
    # legend
    plt.xlabel('Parameters', fontfamily='monospace')
    plt.ylabel('{}'.format(ylabel), fontfamily='monospace')
    plt.legend( ('G++4.9', 'G++9'),
            shadow=False, fontsize=10, frameon=False)
    plt.margins(0,0)
    plt.savefig('./tests/results/grad/graphs/other/random/mitusba_g++49_vs_g++9_{}.pdf'.format(suffix), bbox_inches = 'tight',
        pad_inches = 0)
    plt.clf()



wenzel_static_gcc49, wenzel_dynamic_gcc49 = convert_files_to_lists("./tests/results/grad/json/random/full_results_random-2020-04-12-18:10:23.json", key=gcc_49_key)
wenzel_static_gcc9, wenzel_dynamic_gcc9 = convert_files_to_lists("./tests/results/grad/json/random/full_results_random-2020-04-21-20:37:58.json", key=gcc_9_key)


print("Static 4.9: {}\n Static 9: {}\n".format(wenzel_static_gcc49, wenzel_static_gcc9))
generate_two_graph(wenzel_static_gcc49, wenzel_static_gcc9, num_params, suffix="static", ylabel="Time (s)")
generate_two_graph(wenzel_dynamic_gcc49, wenzel_dynamic_gcc9, num_params, suffix="dynamic", ylabel="Time (s)")