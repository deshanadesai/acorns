import matplotlib.pyplot as plt
import numpy as np
import os
import json
import seaborn as sns
import re

sns.set(style="darkgrid")

num_params_list = [10, 2010, 4010, 6010, 8010, 10010, 20010, 30010, 40010, 50010, 60010, 70010, 80010, 90010 ]

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
    wenzel_static_times = {}
    wenzel_dynamic_times = {}
    enoki_times = {}
    pytorch_times = {}
    us_times = {}
    tapenade_times = {}
    functions = []

    wenzel_static_max = []
    wenzel_dynamic_max = []
    enoki_max = []
    pytorch_max = []
    tapenade_max = []
    us_max = []

    num_params_set = set()
    with open(file_location) as json_data:
        data = json.load(json_data)
        for i, key in enumerate(sorted(data)):
            wenzel_static_times[key] = []
            wenzel_dynamic_times[key] = []
            enoki_times[key] = []
            pytorch_times[key] = []
            us_times[key] = []
            tapenade_times[key] = []
            functions.append(key)

            for num_params in num_params_list:
                num_params_set.add(int(num_params))
                wenzel_static_times[key].append(data[key][num_params]['wenzel_static'])
                wenzel_dynamic_times[key].append(data[key][num_params]['wenzel_dynamic'])
                enoki_times[key].append(data[key][num_params]['enoki'])
                us_times[key].append(data[key][num_params]['us'])
                pytorch_times[key].append(data[key][num_params]['pytorch'])
                tapenade_times[key].append(data[key][num_params]['tapenade'])

            print("{}:{} = {}".format(key, num_params, us_times[key][-1]))
            
            wenzel_static_max.append(wenzel_static_times[key][-1])
            wenzel_dynamic_max.append(wenzel_dynamic_times[key][-1])
            enoki_max.append(enoki_times[key][-1])
            pytorch_max.append(pytorch_times[key][-1])
            us_max.append(us_times[key][-1])
            tapenade_max.append(tapenade_times[key][-1])

    print(num_params_set)
    return wenzel_static_times, wenzel_dynamic_times, enoki_times, pytorch_times, us_times, tapenade_times, functions, num_params_list, wenzel_static_max, wenzel_dynamic_max, enoki_max, pytorch_max, us_max, tapenade_max

def generate_two_graph(avg_us, avg_them, denom, function, label, num_vars):
    plt.plot(denom, avg_us, color='#1abc9c', linestyle='dashed',  markersize=7)
    plt.plot(denom, avg_them, color='#f1c40f', linestyle='dashed', markersize=7)
    # legend
    plt.xlabel('Parameters', fontfamily='monospace')
    plt.ylabel('Time (s)', fontfamily='monospace')
    plt.legend( ('Us', label),
            shadow=False, fontsize=10, frameon=False)
    plt.margins(0,0)
    plt.savefig('./tests/results/grad/graphs/gcc49/non-random/graph_{}_{}.pdf'.format(label, num_vars), bbox_inches = 'tight',
        pad_inches = 0)
    # plt.savefig('./tests/complex/graphs/graph_by_128_speedup.pdf')
    plt.clf()

def generate_full_graph(avg_us, avg_pytorch, avg_wenzel_static, avg_wenzel_dynamic, avg_enoki, avg_tapenade, denom, function, label, num_vars):
    fig = plt.figure(figsize=(20, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(denom, avg_us, color='#1abc9c', linestyle='dashed',  markersize=7)
    ax.plot(denom, avg_pytorch, color='#f1c40f', linestyle='dashed', markersize=7)
    ax.plot(denom, avg_wenzel_static, color='#3498db', linestyle='dashed', markersize=7)
    ax.plot(denom, avg_wenzel_dynamic, color='#34495e', linestyle='dashed', markersize=7)
    ax.plot(denom, avg_enoki, color='#bdc3c7', linestyle='dashed', markersize=7)
    ax.plot(denom, avg_tapenade, color='#2c3e50', linestyle='dashed', markersize=7)
    ax.set_yscale('log')
    # legend
    plt.xlabel('Parameters', fontfamily='monospace')
    plt.ylabel('Time (s)', fontfamily='monospace')
    plt.legend( ('Ours', 'Pytorch', 'Mitsuba (Static)', 'Mitsuba (Dynamic)', 'Enoki', 'Tapenade'),
            shadow=False, fontsize=10, frameon=False)
    plt.margins(0,0)
    plt.savefig('./tests/results/grad/graphs/gcc49/random/graph_{}_full.pdf'.format(num_vars), bbox_inches = 'tight',
        pad_inches = 0)
    plt.clf()

def generate_full_graph_without_dynamic(avg_us, avg_pytorch, avg_wenzel_static, avg_enoki, avg_tapenade, denom, function, label, num_vars):
    fig = plt.figure(figsize=(20, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(denom, avg_us, color='#1abc9c', linestyle='dashed',  markersize=7)
    ax.plot(denom, avg_pytorch, color='#f1c40f', linestyle='dashed', markersize=7)
    ax.plot(denom, avg_wenzel_static, color='#3498db', linestyle='dashed', markersize=7)
    ax.plot(denom, avg_enoki, color='#bdc3c7', linestyle='dashed', markersize=7)
    ax.plot(denom, avg_tapenade, color='#2c3e50', linestyle='dashed', markersize=7)
    ax.set_yscale('log')
    # legend
    plt.xlabel('Parameters', fontfamily='monospace')
    plt.ylabel('Time (s)', fontfamily='monospace')
    plt.legend( ('Ours', 'Pytorch', 'Mitsuba (Static)', 'Enoki', 'Tapenade'),
            shadow=False, fontsize=10, frameon=False)
    plt.margins(0,0)
    plt.savefig('./tests/results/grad/graphs/gcc49/random/graph_{}_full_no_dynamic.pdf'.format(num_vars), bbox_inches = 'tight',
        pad_inches = 0)
    plt.clf()

# def generate_full_graph(avg_us, avg_pytorch, avg_wenzel_static, avg_wenzel_dynamic, avg_enoki, denom, function, label, num_vars):
#     plt.plot(denom, avg_us, color='#1abc9c', linestyle='dashed',  markersize=7)
#     plt.plot(denom, avg_pytorch, color='#f1c40f', linestyle='dashed', markersize=7)
#     plt.plot(denom, avg_wenzel_static, color='#3498db', linestyle='dashed', markersize=7)
#     plt.plot(denom, avg_wenzel_dynamic, color='#34495e', linestyle='dashed', markersize=7)
#     plt.plot(denom, avg_enoki, color='#bdc3c7', linestyle='dashed', markersize=7)
#     # legend
#     plt.xlabel('Parameters', fontfamily='monospace')
#     plt.ylabel('Time (s)', fontfamily='monospace')
#     plt.legend( ('Ours', 'Pytorch', 'Mitsuba (Static)', 'Mitsuba (Dynamic)', 'Enoki'),
#             shadow=False, fontsize=10, frameon=False)
#     plt.margins(0,0)
#     plt.savefig('./tests/results/grad/graphs/gcc49/random/graph_{}_full.pdf'.format(num_vars), bbox_inches = 'tight',
#         pad_inches = 0)
#     plt.clf()

def generate_max_graph(avg_us, avg_pytorch, avg_wenzel_static, avg_wenzel_dynamic, avg_enoki, avg_tapenade, denom):
    fig = plt.figure(figsize=(20, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(denom, avg_us, color='#1abc9c', linestyle='dashed',  markersize=7)
    ax.plot(denom, avg_pytorch, color='#f1c40f', linestyle='dashed', markersize=7)
    ax.plot(denom, avg_wenzel_static, color='#3498db', linestyle='dashed', markersize=7)
    ax.plot(denom, avg_enoki, color='#bdc3c7', linestyle='dashed', markersize=7)
    ax.plot(denom, avg_tapenade, color='#2c3e50', linestyle='dashed', markersize=7)
    ax.set_yscale('log')
    # legend
    plt.xlabel('Variables', fontfamily='monospace')
    plt.ylabel('Time (s)', fontfamily='monospace')
    plt.legend( ('Ours', 'Pytorch', 'Mitsuba (Static)', 'Enoki', 'Tapenade'),
            shadow=False, fontsize=10, frameon=False)
    plt.margins(0,0)
    plt.savefig('./tests/results/grad/graphs/gcc49/random/graph_time_to_variables.pdf', bbox_inches = 'tight',
        pad_inches = 0)
    plt.clf()

wenzel_static_times, wenzel_dynamic_times, enoki_times, pytorch_times, us_times, tapenade_times, functions, num_params, wenzel_static_max, wenzel_dynamic_max, enoki_max, pytorch_max, us_max, tapenade_max = convert_files_to_lists("./tests/results/grad/json/random/full_results_random-2020-04-12-18:10:23.json")

for i, label in enumerate(functions):
    print(us_times[label])
    # generate_two_graph(us_times[label], wenzel_static_times[label], num_params, label, 'Mitsuba(Static)', i)
    # generate_two_graph(us_times[label], wenzel_dynamic_times[label], num_params, label, 'Mitsuba(Dynamic)', i)
    # generate_two_graph(us_times[label], enoki_times[label], num_params, label, 'Enoki', i)
    # generate_two_graph(us_times[label], pytorch_times[label], num_params, label, 'Pytorch', i)
    generate_full_graph(us_times[label], pytorch_times[label], wenzel_static_times[label], wenzel_dynamic_times[label], enoki_times[label], tapenade_times[label], num_params, label, 'Wenzel', i)
    # generate_full_graph_without_dynamic(us_times[label], pytorch_times[label], wenzel_static_times[label], enoki_times[label], tapenade_times[label], num_params, label, 'Wenzel', i)

generate_max_graph(us_max, pytorch_max, wenzel_static_max, wenzel_dynamic_max, enoki_max, tapenade_max, range(1,11))
