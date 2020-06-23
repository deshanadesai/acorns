import matplotlib.pyplot as plt
import numpy as np
import os
import json
import re


fontsize = 19
num_params_list = [10, 2010, 4010, 6010, 8010, 10010, 20010, 30010, 40010]


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
    wenzel_times_hess_static = {}
    us_times_hess = {}
    pytorch_hess_times = {}
    tapenade_hess_times = {}

    functions = []

    wenzel_hess_static_max = []
    tapenade_hess_max = []
    us_max_hess = []
    pytorch_max_hess = []

    with open(file_location) as json_data:
        data = json.load(json_data)

        for key in sorted(data):
            pytorch_hess_times[key] = []
            wenzel_times_hess_static[key] = []
            us_times_hess[key] = []
            tapenade_hess_times[key] = []
            functions.append(key)

            for num_params in num_params_list:
                num_params_str = str(num_params)
                wenzel_times_hess_static[key].append(
                    data[key][num_params_str]['wenzel_static'])
                tapenade_hess_times[key].append(
                    data[key][num_params_str]['tapenade'])
                us_times_hess[key].append(data[key][num_params_str]['us'])
                pytorch_hess_times[key].append(
                    data[key][num_params_str]['pytorch'])

            wenzel_hess_static_max.append(wenzel_times_hess_static[key][-1])
            tapenade_hess_max.append(tapenade_hess_times[key][-1])
            us_max_hess.append(us_times_hess[key][-1])
            pytorch_max_hess.append(pytorch_hess_times[key][-1])
    return us_times_hess, wenzel_times_hess_static, tapenade_hess_times, pytorch_hess_times, \
        functions, num_params_list, \
        us_max_hess, wenzel_hess_static_max, tapenade_hess_max, pytorch_max_hess


def generate_two_graph(avg_us, avg_them, denom, function, label, num_vars):
    plt.plot(denom, avg_us, color='#1abc9c', linestyle='dashed',  markersize=7)
    plt.plot(denom, avg_them, color='#f1c40f',
             linestyle='dashed', markersize=7)
    # legend
    plt.xlabel('Parameters', fontfamily='monospace')
    plt.ylabel('Time (s)', fontfamily='monospace')
    plt.legend(('Us', label),
               shadow=False, fontsize=10, frameon=False)
    plt.margins(0, 0)
    plt.savefig('./tests/results/hess/graphs/random/graph_{}_{}.pdf'.format(label, num_vars), bbox_inches='tight',
                pad_inches=0)
    # plt.savefig('./tests/complex/graphs/graph_by_128_speedup.pdf')
    plt.clf()


def generate_four_graph(avg_us, avg_wenzel_static, avg_tapenade, avg_pytorch, denom, num_vars):
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(denom, avg_us, color='#130f40',
            linestyle='dashed',  markersize=7)
    ax.plot(denom, avg_wenzel_static, color='#ff7979',
            linestyle='dashed', markersize=7)
    ax.plot(denom, avg_tapenade, color='#badc58',
            linestyle='dashed', markersize=7)
    ax.plot(denom, avg_pytorch, color='#7ed6df',
            linestyle='dashed', markersize=7)
    ax.set_yscale('log')
    plt.ylim(1.e-05, 1.e+03)
    plt.xlim(2010, 40010)
    plt.setp(ax.get_xticklabels(), fontsize=20)
    plt.setp(ax.get_yticklabels(), fontsize=20)
    # legend
    plt.legend(('ACORNS', 'Mitsuba (Static)', 'Tapenade', 'PyTorch'),
               shadow=False, fontsize=fontsize, frameon=False)
    plt.margins(0, 0)
    plt.savefig('./tests/results/hess/graphs/random/full/graph_{}_full_hess_g++9.pdf'.format(num_vars), bbox_inches='tight',
                pad_inches=0)
    plt.clf()

def generate_max_graph(max_us_hess, max_wenzel_hess_static, max_tapenade_hess, max_pytorch, denom):
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(denom, max_us_hess, color='#130f40',
            linestyle='dashed',  markersize=7)
    ax.plot(denom, max_wenzel_hess_static, color='#ff7979',
            linestyle='dashed', markersize=7)
    ax.plot(denom, max_tapenade_hess, color='#badc58',
            linestyle='dashed', markersize=7)
    ax.plot(denom, max_pytorch, color='#7ed6df',
            linestyle='dashed', markersize=7)
    ax.set_yscale('log')
    plt.ylim(1.e-05, 1.e+03)
    plt.setp(ax.get_xticklabels(), fontsize=20)
    plt.setp(ax.get_yticklabels(), fontsize=20)
    # legend
    plt.legend(('ACORNS', 'Mitsuba (Static)', 'Tapenade', 'PyTorch'),
               shadow=False, fontsize=fontsize, frameon=False)
    plt.margins(0, 0)
    plt.savefig('./tests/results/hess/graphs/random/max/graph_max_hess_g++9.pdf', bbox_inches='tight',
                pad_inches=0)
    plt.clf()


file_location = "./tests/results/hess/json/random/full_results_hessian-2020-06-20-07:20:31.json"

us_times_hess, wenzel_times_hess_static, tapenade_times_hess, pytorch_times_hess, \
functions, num_params, \
us_max_hess, wenzel_hess_static_max, tapenade_max_times, pytorch_max_hess = convert_files_to_lists(
        file_location)

for i, label in enumerate(functions):
    # print(wenzel_times_hess_static[label])
    generate_four_graph(us_times_hess[label], wenzel_times_hess_static[label],
                        tapenade_times_hess[label], pytorch_times_hess[label], num_params, i)

print("Us: {}\n Wenzel: {}\n Tape: {}\n Py:{}".format(us_max_hess, wenzel_hess_static_max, tapenade_max_times, pytorch_max_hess))

generate_max_graph(us_max_hess, wenzel_hess_static_max,
                   tapenade_max_times, pytorch_max_hess, range(1, 11))
