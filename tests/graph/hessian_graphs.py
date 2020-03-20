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
    wenzel_times_grad = {}
    wenzel_times_hess = {}
    us_times_grad = {}
    us_times_hess = {}
    functions = []
    num_params_set = set()
    with open(file_location) as json_data:
        data = json.load(json_data)
        for i, key in enumerate(data):
            wenzel_times_grad[key] = []
            wenzel_times_hess[key] = []
            us_times_grad[key] = []
            us_times_hess[key] = []
            functions.append(key)
            for num_params in sorted(data[key],key=natural_keys):
                num_params_set.add(int(num_params))
                wenzel_times_grad[key].append(data[key][num_params]['wenzel_grad'])
                wenzel_times_hess[key].append(data[key][num_params]['wenzel_hess'])
                us_times_grad[key].append(data[key][num_params]['us_grad'])
                us_times_hess[key].append(data[key][num_params]['us_hessian'])
    print(num_params_set)
    num_params_list = list(sorted(num_params_set))
    return wenzel_times_grad, wenzel_times_hess, us_times_grad, us_times_hess, functions, num_params_list

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
    plt.savefig('results/hess/graph_{}_{}.png'.format(label, num_vars))
    plt.clf()

def generate_full_graph(avg_us_grad, avg_wenzel_grad, avg_us_hess, avg_wenzel_hess, denom, function, label, num_vars):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(denom, avg_us_grad,
             denom, avg_wenzel_grad,
             denom, avg_us_hess,
             denom, avg_wenzel_hess)
    # plt.xticks(denom)
    plt.title('Us Grad vs Mitsuba Grad vs Us Hess vs Mitsuba Hess # It: 10')
    # legend
    plt.legend( ('Us Grad', 'Mitsuba Grad', 'Us Hess', 'Mitsuba Hess'),
            shadow=True, loc=(0.01, 0.48), handlelength=1.5, fontsize=10)
    plt.xlabel('# params')
    plt.ylabel('time (s)')
    plt.tight_layout()
    plt.figtext(0.99, 0.01, "y={}".format(function), horizontalalignment='right', fontsize=5)
    plt.savefig('results/hess/graph_{}_full.png'.format(num_vars))
    plt.clf()

wenzel_times_grad, wenzel_times_hess, us_times_grad, us_times_hess, functions, num_params = convert_files_to_lists("./results/hess/full_results_hessian.json")

for i, label in enumerate(functions):
    generate_two_graph(us_times_grad[label], wenzel_times_grad[label], num_params, label, 'Mitsuba Gradient', i)
    generate_two_graph(us_times_hess[label], wenzel_times_hess[label], num_params, label, 'Mitsuba Hessian', i)
    generate_full_graph(us_times_grad[label], wenzel_times_grad[label], us_times_hess[label], wenzel_times_hess[label], num_params, label, 'Wenzel', i)
