import matplotlib.pyplot as plt
import numpy as np
import os
import json
import seaborn as sns
import re

sns.set(style="darkgrid")

labels = ['3D_P1_non_zero', '3D_P2_non_zero', '3D_P3_non_zero', '3D_P4_non_zero']

def atoi(text):
    return int(text) if text.isdigit() else text
def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def convert_files_to_lists(file_location):
    runtimes = []
    wenzel_static = []
    wenzel_dynamic = []
    num_vars = []
    with open(file_location) as json_data:
        data = json.load(json_data)
        for key in sorted(data):
            if key in labels:
                runtimes.append(data[key]['us'])
                wenzel_static.append(data[key]['avg_runtime_static'])
                wenzel_dynamic.append(data[key]['avg_runtime_dynamic'])
                num_vars.append(data[key]['local_disp_size'])
    return runtimes, wenzel_static, wenzel_dynamic, num_vars

def get_speedup(us, other):
    return [other[i] / us[i] for i in range(len(us))]

def generate_two_graph(avg_us, wenzel_static, wenzel_dynamic, denom):
    fig = plt.figure(figsize=(20, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(denom, avg_us, color='#1abc9c', linestyle='dashed',  markersize=7)
    ax.plot(denom, wenzel_static, color='#f1c40f', linestyle='dashed', markersize=7)
    ax.plot(denom, wenzel_dynamic, color='#3498db', linestyle='dashed', markersize=7)
    ax.set_yscale('log')
    # legend
    plt.xlabel('Variables', fontfamily='monospace')
    plt.ylabel('Time (s)', fontfamily='monospace')
    plt.legend( ('Ours', 'Mitsuba (Static)', 'Mitsuba (Dynamic)'),
            shadow=False, fontsize=10, frameon=False)
    plt.margins(0,0)
    plt.savefig('./tests/complex/graphs/runs/us_vs_wenzel_raw.pdf', bbox_inches = 'tight',
        pad_inches = 0)
    plt.clf()

def generate_speedup_graph(wenzel_static, wenzel_dynamic, denom):
    fig = plt.figure(figsize=(20, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(denom, wenzel_static, color='#f1c40f', linestyle='dashed', markersize=7)
    ax.plot(denom, wenzel_dynamic, color='#3498db', linestyle='dashed', markersize=7)
    ax.set_yscale('log')
    # legend
    plt.xlabel('Variables', fontfamily='monospace')
    plt.ylabel('Speedup (%)', fontfamily='monospace')
    plt.legend( ('Mitsuba (Static)', 'Mitsuba (Dynamic)'),
            shadow=False, fontsize=10, frameon=False)
    plt.margins(0,0)
    plt.savefig('./tests/complex/graphs/runs/our_speedup.pdf', bbox_inches = 'tight',
        pad_inches = 0)
    plt.clf()

runtimes, wenzel_static, wenzel_dynamic, num_vars = convert_files_to_lists("./tests/complex/wenzel/final_results.json")
generate_two_graph(runtimes, wenzel_static, wenzel_dynamic, num_vars)
static_speedup = get_speedup(runtimes, wenzel_static)
dynamic_speedup = get_speedup(runtimes, wenzel_dynamic)
print(static_speedup, dynamic_speedup)
generate_speedup_graph(wenzel_static, wenzel_dynamic, num_vars)