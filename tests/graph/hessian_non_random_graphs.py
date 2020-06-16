import matplotlib.pyplot as plt
import numpy as np
import os
import json
import re

num_params_list = [10, 2010, 4010, 6010, 8010, 10010, 20010, 30010, 40010]
fontsize = 19


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
    # wenzel_times_grad_static = {}
    # wenzel_times_grad_dynamic = {}
    wenzel_times_hess_static = {}
    wenzel_times_hess_dynamic = {}
    # us_times_grad = {}
    us_times_hess = {}
    pytorch_hess_times = {}
    functions = []

    # wenzel_grad_static_max = []
    # wenzel_grad_dynamic_max = []
    wenzel_hess_static_max = []
    wenzel_hess_dynamic_max = []
    # us_max_grad = []
    us_max_hess = []
    pytorch_max_hess = []

    with open(file_location) as json_data:
        data = json.load(json_data)

        for i, key in enumerate(sorted(data)):
            pytorch_hess_times[key] = []
            # wenzel_times_grad_static[key] = []
            # wenzel_times_grad_dynamic[key] = []
            wenzel_times_hess_static[key] = []
            wenzel_times_hess_dynamic[key] = []
            # us_times_grad[key] = []
            us_times_hess[key] = []
            functions.append(key)

            for num_params in num_params_list:
                num_params_str = str(num_params)
                # wenzel_times_grad_static[key].append(data[key][num_params_str]['wenzel_grad_static'])
                # wenzel_times_grad_dynamic[key].append(data[key][num_params_str]['wenzel_grad_dynamic'])
                wenzel_times_hess_static[key].append(
                    data[key][num_params_str]['wenzel_static'])
                wenzel_times_hess_dynamic[key].append(
                    data[key][num_params_str]['wenzel_dynamic'])
                # us_times_grad[key].append(data[key][num_params_str]['us_grad'])
                us_times_hess[key].append(data[key][num_params_str]['us'])
                pytorch_hess_times[key].append(
                    data[key][num_params_str]['pytorch'])
            # wenzel_grad_static_max.append(wenzel_times_grad_static[key][-1])
            # wenzel_grad_dynamic_max.append(wenzel_times_grad_dynamic[key][-1])
            wenzel_hess_static_max.append(wenzel_times_hess_static[key][-1])
            wenzel_hess_dynamic_max.append(wenzel_times_hess_dynamic[key][-1])
            # us_max_grad.append(us_times_grad[key][-1])
            us_max_hess.append(us_times_hess[key][-1])
            pytorch_max_hess.append(pytorch_hess_times[key][-1])
    return wenzel_times_hess_static, wenzel_times_hess_dynamic, us_times_hess, \
        functions, num_params_list, wenzel_hess_static_max, wenzel_hess_dynamic_max, us_max_hess, \
        pytorch_hess_times, pytorch_max_hess


def generate_four_graph(avg_us, avg_wenzel_static, avg_wenzel_dynamic, avg_pytorch, denom, num_vars):
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(denom, avg_us, color='#130f40',
            linestyle='dashed',  markersize=7)
    ax.plot(denom, avg_wenzel_static, color='#ff7979',
            linestyle='dashed', markersize=7)
    ax.plot(denom, avg_wenzel_dynamic, color='#badc58',
            linestyle='dashed', markersize=7)
    ax.plot(denom, avg_pytorch, color='#7ed6df',
            linestyle='dashed', markersize=7)
    ax.set_yscale('log')
    plt.ylim(1.e-05, 1.e+02)
    plt.xlim(2010, 40010)
    plt.setp(ax.get_xticklabels(), fontsize=20)
    plt.setp(ax.get_yticklabels(), fontsize=20)
    # legend
    plt.legend(('ACORNS', 'Mitsuba (Static)', 'Mitsuba (Dynamic)', 'PyTorch'),
               shadow=False, fontsize=fontsize, frameon=False)
    plt.margins(0, 0)
    plt.savefig('./tests/results/hess/graphs/non-random/full/{}_function_hess_g++9.pdf'.format(num_vars), bbox_inches='tight',
                pad_inches=0)
    plt.clf()


file_location = "./tests/results/hess/json/full_results_hessian-2020-05-21-18:50:14.json"

wenzel_times_hess_static, wenzel_times_hess_dynamic, us_times_hess, functions, num_params, \
    wenzel_hess_static_max, wenzel_hess_dynamic_max, us_max_hess, \
    pytorch_hess_times, pytorch_max_hess = convert_files_to_lists(
        file_location)

for i, label in enumerate(functions):
    # print(wenzel_times_hess_static[label])
    generate_four_graph(us_times_hess[label], wenzel_times_hess_static[label],
                        wenzel_times_hess_dynamic[label], pytorch_hess_times[label], num_params, i)

print("Us: {}\n Wenzel Static: {}\n Wenzel Dynamic: {}".format(
    us_max_hess, wenzel_hess_static_max, wenzel_hess_dynamic_max))
