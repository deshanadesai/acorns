import matplotlib.pyplot as plt
import numpy as np
import os
import json
import re

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
    wenzel_times = {}
    enoki_times = {}
    pytorch_times = {}
    us_times = {}
    functions = []

    wenzel_max = []
    enoki_max = []
    pytorch_max = []
    us_max = []

    num_params_set = set()
    with open(file_location) as json_data:
        data = json.load(json_data)
        for i, key in enumerate(data):
            wenzel_times[key] = []
            enoki_times[key] = []
            pytorch_times[key] = []
            us_times[key] = []
            functions.append(key)

            for num_params in sorted(data[key],key=natural_keys):
                num_params_set.add(int(num_params))
                wenzel_times[key].append(data[key][num_params]['wenzel'])
                enoki_times[key].append(data[key][num_params]['enoki'])
                us_times[key].append(data[key][num_params]['us'])
                pytorch_times[key].append(data[key][num_params]['pytorch'])
            
            wenzel_max.append(wenzel_times[key][-1])
            enoki_max.append(enoki_times[key][-1])
            pytorch_max.append(pytorch_times[key][-1])
            us_max.append(us_times[key][-1])

    print(num_params_set)
    num_params_list = list(sorted(num_params_set))
    return wenzel_times, enoki_times, pytorch_times, us_times, functions, num_params_list, wenzel_max, enoki_max, pytorch_max, us_max

def generate_two_graph(avg_us, avg_them, denom, function, label, num_vars):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(denom, avg_us, '-bo',
             denom, avg_them, '-go')
    # plt.xticks(denom)
    plt.title('Us vs {} # It: 10'.format(label))
    # legend
    plt.legend( ('Ours', label),
            shadow=True, loc=(0.01, 0.48), handlelength=1.5, fontsize=10)
    plt.xlabel('# params')
    plt.ylabel('time (s)')
    plt.tight_layout()
    plt.figtext(0.99, 0.01, "y={}".format(function), horizontalalignment='right', fontsize=5)
    plt.savefig('./tests/results/grad/graphs/graph_{}_{}.png'.format(label, num_vars))
    plt.clf()

def generate_full_graph(avg_us, avg_pytorch, avg_wenzel, avg_enoki, denom, function, label, num_vars):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(denom, avg_us,
             denom, avg_pytorch,
             denom, avg_wenzel,
             denom, avg_enoki)
    # plt.xticks(denom)
    plt.title('Us vs Pytorch vs Wenzel vs Enoki # It: 10')
    # legend
    plt.legend( ('Ours', 'Pytorch', 'Wenzel', 'Enoki'),
            shadow=True, loc=(0.01, 0.48), handlelength=1.5, fontsize=10)
    plt.xlabel('# params')
    plt.ylabel('time (s)')
    plt.tight_layout()
    plt.figtext(0.99, 0.01, "y={}".format(function), horizontalalignment='right', fontsize=5)
    plt.savefig('./tests/results/grad/graphs/graph_{}_full.png'.format(num_vars))
    plt.clf()

def generate_max_graph(avg_us, avg_pytorch, avg_wenzel, avg_enoki, denom):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(denom, avg_us,
             denom, avg_pytorch,
             denom, avg_wenzel,
             denom, avg_enoki)
    # plt.xticks(denom)
    plt.title('Us vs Pytorch vs Wenzel vs Enoki # It: 10')
    # legend
    plt.legend( ('Ours', 'Pytorch', 'Wenzel', 'Enoki'),
            shadow=True, loc=(0.01, 0.48), handlelength=1.5, fontsize=10)
    plt.xlabel('# vars')
    plt.ylabel('time (s)')
    plt.tight_layout()
    plt.savefig('./tests/results/grad/graphs/graph_max.png')
    plt.clf()

wenzel_times, enoki_times, pytorch_times, us_times, functions, num_params, wenzel_max, enoki_max, pytorch_max, us_max = convert_files_to_lists("./tests/results/grad/full_results_random.json")

for i, label in enumerate(functions):
    print(us_times[label])
    generate_two_graph(us_times[label], wenzel_times[label], num_params, label, 'Wenzel', i)
    generate_two_graph(us_times[label], enoki_times[label], num_params, label, 'Enoki', i)
    generate_two_graph(us_times[label], pytorch_times[label], num_params, label, 'Pytorch', i)
    generate_full_graph(us_times[label], pytorch_times[label], wenzel_times[label], enoki_times[label], num_params, label, 'Wenzel', i)

generate_max_graph(us_max, pytorch_max, wenzel_max, enoki_max, range(1,10))
