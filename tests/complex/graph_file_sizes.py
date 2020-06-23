import matplotlib.pyplot as plt
import numpy as np
import os
import json
import math
import re

fontsize = 30
num_params = [78, 465, 465, 1830, 5565]


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def convert_split_size_to_number_of_files(split_sizes, num_params):
    num_files = []
    for split in split_sizes:
        num_file = math.ceil(float(num_params) / float(split))
        num_files.append(num_file)
    return num_files


def convert_files_to_lists(file_location):
    o_sizes = {}
    functions = []

    split_set = set()
    with open(file_location) as json_data:
        data = json.load(json_data)
        for key in sorted(data):
            o_sizes[key] = []
            functions.append(key)

            for split in sorted(data[key], key=natural_keys):
                if '.o' in data[key][split]:
                    o_size = float(data[key][split]['.o'] / 1e+9)
                    split_set.add(int(split))
                    print("Key: {}, Split: {}, Data: {} ".format(
                        key, split, data[key][split]))
                    # print("C Size is {} GB".format(c_size))
                    # print("O Size is {} GB".format(o_size))
                    o_sizes[key].append(o_size)

    print(split_set)
    split_list = list(sorted(split_set))
    return o_sizes, functions, split_list


def generate_two_graph(avg_us, denom, function, suffix="", ymin=1.e+00, ymax=1.e+02):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(denom, avg_us, color='#1abc9c', linestyle='dashed',  markersize=7)
    plt.ylim(ymin, ymax)
    plt.setp(ax.get_xticklabels(), fontsize=20)
    plt.setp(ax.get_yticklabels(), fontsize=20)
    plt.yscale('log')
    plt.margins(0, 0)
    plt.savefig('./tests/complex/graphs/sizes/{}-{}.pdf'.format(function, suffix), bbox_inches='tight',
                pad_inches=0)

    plt.clf()


o_sizes, functions, split_list, = convert_files_to_lists(
    "./tests/complex/data/sizes/file_sizes.json")

for i, function in enumerate(functions):
    num_files = convert_split_size_to_number_of_files(
        split_list, num_params[i])
    print('{}: \n O Sizes: {}\n Num Files {}'.format(
        function, o_sizes[function], num_files))
    generate_two_graph(o_sizes[function], num_files,
                       function, suffix="O", ymin=1.e-04, ymax=1.e-02)
    # generate_full_graph_without_dynamic(us_times[label], pytorch_times[label], wenzel_static_times[label], enoki_times[label], tapenade_times[label], num_params, label, 'Wenzel', i)
