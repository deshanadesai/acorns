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
    us_file_gen_times = []
    us_compile_times = []
    tapenade_file_gen_times = []
    tapenade_compile_times = []

    functions = []

    with open(file_location) as json_data:
        data = json.load(json_data)

        for key in sorted(data):
            functions.append(key)
            us_file_gen_times.append(data[key]['us_file_gen'])
            us_compile_times.append(data[key]['us_compile_time'])
            tapenade_file_gen_times.append(data[key]['tapenade_file_gen'])
            tapenade_compile_times.append(data[key]['tapenade_compile_time'])

    return us_file_gen_times, us_compile_times, tapenade_file_gen_times, tapenade_compile_times, functions


def generate_two_graph(avg_us, avg_them, denom, label):
    plt.plot(denom, avg_us, color='#1abc9c', linestyle='dashed',  markersize=7)
    plt.plot(denom, avg_them, color='#f1c40f',
             linestyle='dashed', markersize=7)
    # legend
    plt.legend(('Us', 'Tapenade'),
               shadow=False, fontsize=10, frameon=False)
    plt.margins(0, 0)
    plt.savefig('./tests/results/hess/graphs/random/{}.pdf'.format(label), bbox_inches='tight',
                pad_inches=0)
    plt.clf()


file_location = "./tests/results/hess/json/random/compile_and_file_gen_times.json"

us_file_gen_times, us_compile_times, tapenade_file_gen_times, tapenade_compile_times, functions = convert_files_to_lists(
    file_location)

print(us_file_gen_times)

for function in functions:
    # print(wenzel_times_hess_static[label])
    generate_two_graph(us_file_gen_times, tapenade_file_gen_times, range(
        1, 11), 'file_gen_times')
    generate_two_graph(us_compile_times, tapenade_compile_times, range(
        1, 11), 'compile_times')
