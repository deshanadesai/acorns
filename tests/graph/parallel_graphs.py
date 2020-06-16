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
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def convert_files_to_lists(file_location):
    our_times = []
    with open(file_location) as json_data:
        data = json.load(json_data)
        for i, key in enumerate(sorted(data)):
            for num_cores in sorted(data[key], key=natural_keys):
                our_times.append(data[key][num_cores]['us'])
    return our_times


def get_speedup_list(time_list):
    speedup_list = []
    single_thread_time = time_list[0]
    for time in time_list[1:]:
        speedup_list.append(float(single_thread_time) / float(time))
    return speedup_list


def generate_two_graph(avg_us, denom, suffix="", ylabel="Time (s)"):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(denom, avg_us, color='#1abc9c', linestyle='dashed',  markersize=7)
    plt.margins(0, 0)
    plt.xlim(1, 47)
    plt.setp(ax.get_xticklabels(), fontsize=20)
    plt.setp(ax.get_yticklabels(), fontsize=20)
    plt.savefig('./tests/results/hess/graphs/parallel/parallel-graph{}.pdf'.format(suffix), bbox_inches='tight',
                pad_inches=0)
    # plt.savefig('./tests/complex/graphs/graph_by_128_speedup.pdf')
    plt.clf()


our_times = convert_files_to_lists(
    "./tests/results/grad/json/parallel/parallel_results_good.json")

print(our_times)

generate_two_graph(our_times, range(1, 48))

speedup_list = get_speedup_list(our_times)
generate_two_graph(speedup_list, range(1, 47), suffix="-speedup",
                   ylabel="Speedup (Time Single Thread / Time X Threads)")
