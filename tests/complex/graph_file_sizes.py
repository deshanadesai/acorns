import matplotlib.pyplot as plt
import numpy as np
import os
import json
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

def generate_two_graph(avg_us, denom, function, suffix=""):
    plt.plot(denom, avg_us, color='#1abc9c', linestyle='dashed',  markersize=7)
    # legend
    plt.xlabel('Number of Lines per File', fontfamily='monospace')
    plt.ylabel('File Size (b)', fontfamily='monospace')
    plt.margins(0,0)
    plt.savefig('./tests/complex/graphs/sizes/{}-{}.pdf'.format(function, suffix), bbox_inches = 'tight',
        pad_inches = 0)

    plt.clf()

c_sizes, o_sizes, functions, split_list, = convert_files_to_lists("./tests/complex/data/sizes/file_sizes.json")

for function in functions:
    generate_two_graph(c_sizes[function], split_list, function, suffix="C")
    generate_two_graph(o_sizes[function], split_list, function, suffix="O")
    # generate_full_graph_without_dynamic(us_times[label], pytorch_times[label], wenzel_static_times[label], enoki_times[label], tapenade_times[label], num_params, label, 'Wenzel', i)
