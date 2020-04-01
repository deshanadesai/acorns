import matplotlib.pyplot as plt
import numpy as np
import os
import json
import re
import seaborn as sns
import re

sns.set(style="darkgrid")

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
    tapenade_times = {}
    us_times = {}
    functions = []

    tapenade_max = []
    us_max = []

    num_params_set = set()
    with open(file_location) as json_data:
        data = json.load(json_data)
        for i, key in enumerate(sorted(data)):
            tapenade_times[key] = []
            us_times[key] = []
            functions.append(key)

            for num_params in sorted(data[key],key=natural_keys):
                num_params_set.add(int(num_params))
                tapenade_times[key].append(data[key][num_params]['tapenade'])
                us_times[key].append(data[key][num_params]['us'])

            print("{}:{} = {}".format(key, num_params, us_times[key][-1]))
            
            tapenade_max.append(tapenade_times[key][-1])
            us_max.append(us_times[key][-1])

    print(num_params_set)
    num_params_list = list(sorted(num_params_set))
    return tapenade_times, us_times, functions, num_params_list

def generate_two_graph(avg_us, avg_them, denom, function, label, num_vars):
    plt.plot(denom, avg_us, color='#1abc9c', linestyle='dashed',  markersize=7)
    plt.plot(denom, avg_them, color='#f1c40f', linestyle='dashed', markersize=7)
    # legend
    plt.xlabel('Parameters', fontfamily='monospace')
    plt.ylabel('Time (s)', fontfamily='monospace')
    plt.legend( ('Us', 'Tapenade'),
            shadow=False, fontsize=10, frameon=False)
    plt.figtext(0.99, 0.01, "y={}".format(function), horizontalalignment='right', fontsize=5)
    plt.margins(0,0)
    plt.savefig("./tests/results/grad/graphs/tapenade.pdf", bbox_inches = 'tight',
        pad_inches = 0)
    # plt.savefig('./tests/complex/graphs/graph_by_128_speedup.pdf')
    plt.clf()

def generate_full_graph(avg_us, avg_pytorch, avg_wenzel_static, avg_wenzel_dynamic, avg_enoki, denom, function, label, num_vars):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(denom, avg_us,
             denom, avg_pytorch,
             denom, avg_wenzel_static,
             denom, avg_wenzel_dynamic,
             denom, avg_enoki)
    # plt.xticks(denom)
    plt.title('Us vs Pytorch vs Mitsuba vs Enoki # It: 10')
    # legend
    plt.legend( ('Ours', 'Pytorch', 'Mitsuba (Static)', 'Mitsuba (Dynamic)', 'Enoki'),
            shadow=True, loc=(0.01, 0.48), handlelength=1.5, fontsize=10)
    plt.xlabel('# params')
    plt.ylabel('time (s)')
    plt.tight_layout()
    plt.figtext(0.99, 0.01, "y={}".format(function), horizontalalignment='right', fontsize=5)
    plt.savefig('./tests/results/grad/graphs/gcc49/graph_{}_full.png'.format(num_vars))
    plt.clf()

def generate_max_graph(avg_us, avg_pytorch, avg_wenzel_static, avg_wenzel_dynamic, avg_enoki, denom):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(denom, avg_us,
             denom, avg_pytorch,
             denom, avg_wenzel_static,
             denom, avg_wenzel_dynamic,
             denom, avg_enoki)
    # plt.xticks(denom)
    plt.title('Us vs Pytorch vs Mitsuba vs Enoki # It: 10')
    # legend
    plt.legend( ('Ours', 'Pytorch', 'Mitsuba (Static)', 'Mitsuba (Dynamic)', 'Enoki'),
            shadow=True, loc=(0.01, 0.48), handlelength=1.5, fontsize=10)
    plt.xlabel('# vars')
    plt.ylabel('time (s)')
    plt.tight_layout()
    plt.savefig('./tests/results/grad/graphs/gcc49/graph_max.png')
    plt.clf()

tapenade_times, us_times, functions, num_params = convert_files_to_lists("tests/results/grad/full_results-tapenade-2020-03-31-19:36:34.json")

for i, label in enumerate(functions):
#     print(us_times[label])
    generate_two_graph(us_times[label], tapenade_times[label], num_params, label, 'Tapenade', i)
#     generate_two_graph(us_times[label], wenzel_dynamic_times[label], num_params, label, 'Mitsuba (Dynamic)', i)
#     generate_two_graph(us_times[label], enoki_times[label], num_params, label, 'Enoki', i)
#     generate_two_graph(us_times[label], pytorch_times[label], num_params, label, 'Pytorch', i)
#     generate_full_graph(us_times[label], pytorch_times[label], wenzel_static_times[label], wenzel_dynamic_times[label], enoki_times[label], num_params, label, 'Wenzel', i)

# generate_max_graph(us_max, pytorch_max, wenzel_static_max, wenzel_dynamic_max, enoki_max, range(1,10))
