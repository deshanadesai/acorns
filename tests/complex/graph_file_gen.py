import matplotlib.pyplot as plt
import numpy as np
import os
import json
import re

fontsize = 30
num_params = [78, 465, 465, 1830]


def convert_split_size_to_number_of_files(split_sizes, num_params):
    num_files = []
    for split in split_sizes:
        num_file = math.ceil(float(num_params) / float(split))
        num_files.append(num_file)
    return num_files

def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def convert_files_to_lists(file_location):
    file_gen_times = {}
    functions = []

    split_set = set()
    with open(file_location) as json_data:
        data = json.load(json_data)
        for key in sorted(data):
            file_gen_times[key] = []
            functions.append(key)

            for split in sorted(data[key], key=natural_keys):
                split_set.add(int(split))
                file_gen_times[key].append(data[key][split]['total_time'])

    print(split_set)
    split_list = list(sorted(split_set))
    return file_gen_times, functions, split_list


def generate_two_graph(avg_us, denom, function, suffix=""):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(denom, avg_us, color='#1abc9c', linestyle='dashed',  markersize=7)
    plt.ylim(1.e+01, 1.e+05)
    plt.setp(ax.get_xticklabels(), fontsize=20)
    plt.setp(ax.get_yticklabels(), fontsize=20)
    plt.yscale('log')
    plt.margins(0, 0)
    plt.savefig('./tests/complex/graphs/file_gen/{}-{}.pdf'.format(function, suffix), bbox_inches='tight',
                pad_inches=0)
    plt.clf()


file_gen_times, functions, split_list, = convert_files_to_lists(
    "./tests/complex/data/file_gen/file_gen_times.json")

for function in functions:
    # generate_two_graph(runtimes[function], split_list, function, suffix="Runtimes")
    generate_two_graph(file_gen_times[function],
                       split_list, function, suffix="Gen_Times")
    # generate_full_graph_without_dynamic(us_times[label], pytorch_times[label], wenzel_static_times[label], enoki_times[label], tapenade_times[label], num_params, label, 'Wenzel', i)
