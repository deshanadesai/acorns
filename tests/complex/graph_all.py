import matplotlib.pyplot as plt
import numpy as np
import os
import json
import seaborn as sns
import re

sns.set(style="darkgrid")

keys = ['3D_P1_non_zero', '3D_P2_non_zero', '3D_P3_non-zero']

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def get_file_sizes(file_location):
    c_sizes = {}
    o_sizes = {}
    functions = []

    split_set = set()
    with open(file_location) as json_data:
        data = json.load(json_data)
        for key in sorted(data):
            c_sizes[key] = []
            o_sizes[key] = []
            functions.append(key)

            for split in sorted(data[key],key=natural_keys):
                split_set.add(int(split))
                print("Key: {}, Split: {}, Data: {}".format(key, split, data[key][split]))
                c_sizes[key].append(data[key][split]['.c'])
                o_sizes[key].append(data[key][split]['.o'])

    print(split_set)
    split_list = list(sorted(split_set))
    return c_sizes, o_sizes, functions, split_list

def get_run_and_compile_times(file_location):
    runtimes = {}
    compile_times = {}
    functions = []

    split_set = set()
    with open(file_location) as json_data:
        data = json.load(json_data)
        for key in sorted(data):
            runtimes[key] = []
            compile_times[key] = []
            functions.append(key)

            for split in sorted(data[key],key=natural_keys):
                split_set.add(int(split))
                print("Key: {}, Split: {}, Data: {}".format(key, split, data[key][split]))
                runtimes[key].append(data[key][split]['us'])
                compile_times[key].append(data[key][split]['compile_time'])

    print(split_set)
    split_list = list(sorted(split_set))
    return runtimes, compile_times

def generate_two_graph(avg_us, denom, function, suffix=""):
    plt.plot(denom, avg_us, color='#1abc9c', linestyle='dashed',  markersize=7)
    # legend
    plt.xlabel('Number of Lines per File', fontfamily='monospace')
    plt.ylabel('File Size (b)', fontfamily='monospace')
    plt.margins(0,0)

c_sizes, o_sizes, functions, split_list = get_file_sizes("./tests/complex/data/sizes/file_sizes.json")
runtimes, compile_times = get_run_and_compile_times("./tests/complex/data/runs/data.json")

fig = plt.figure(figsize=(20, 20))
axs = fig.subplots(3, 4)
# fig.tight_layout()
for i, key in enumerate(keys):
    print(key)
    axs[i, 0].plot(split_list, c_sizes[key])
    axs[i, 0].set_title('Size of C Files {}'.format(key), fontsize=10)
    # axs.xlabel('Number of Lines per File', fontfamily='monospace')
    # plt.ylabel('File Size (b)', fontfamily='monospace')
    axs[i, 1].plot(split_list, o_sizes[key])
    axs[i, 1].set_title('Size of Binaries {}'.format(key), fontsize=10)
    axs[i, 2].plot(split_list, compile_times[key])
    axs[i, 2].set_title('Compilation of {}'.format(key), fontsize=10)
    axs[i, 3].plot(split_list, runtimes[key])
    axs[i, 3].set_title('Runtimes of {}'.format(key), fontsize=10)
plt.margins(0,0)
plt.savefig('./tests/complex/graphs/same_graph.png')
plt.clf()

# for function in functions:
#     generate_two_graph(runtimes[function], split_list, function, suffix="C")
#     generate_two_graph(compile_times[function], split_list, function, suffix="O")
#     # generate_full_graph_without_dynamic(us_times[label], pytorch_times[label], wenzel_static_times[label], enoki_times[label], tapenade_times[label], num_params, label, 'Wenzel', i)
