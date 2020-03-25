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
    wenzel_times_grad_static = {}
    wenzel_times_grad_dynamic = {}
    wenzel_times_hess_static = {}
    wenzel_times_hess_dynamic = {}
    us_times_grad = {}
    us_times_hess = {}
    functions = []


    wenzel_grad_static_max = []
    wenzel_grad_dynamic_max = []
    wenzel_hess_static_max = []
    wenzel_hess_dynamic_max = []
    us_max_grad = []
    us_max_hess = []

    num_params_set = set()
    with open(file_location) as json_data:
        data = json.load(json_data)
        for i, key in enumerate(sorted(data)):
            wenzel_times_grad_static[key] = []
            wenzel_times_grad_dynamic[key] = []
            wenzel_times_hess_static[key] = []
            wenzel_times_hess_dynamic[key] = []
            us_times_grad[key] = []
            us_times_hess[key] = []
            functions.append(key)

            for num_params in sorted(data[key],key=natural_keys):
                num_params_set.add(int(num_params))
                wenzel_times_grad_static[key].append(data[key][num_params]['wenzel_grad_static'])
                wenzel_times_grad_dynamic[key].append(data[key][num_params]['wenzel_grad_dynamic'])
                wenzel_times_hess_static[key].append(data[key][num_params]['wenzel_hess_dynamic'])
                wenzel_times_hess_dynamic[key].append(data[key][num_params]['wenzel_hess_dynamic'])
                us_times_grad[key].append(data[key][num_params]['us_grad'])
                us_times_hess[key].append(data[key][num_params]['us_hessian'])
            wenzel_grad_static_max.append(wenzel_times_grad_static[key][-1])
            wenzel_grad_dynamic_max.append(wenzel_times_grad_dynamic[key][-1])
            wenzel_hess_static_max.append(wenzel_times_hess_static[key][-1])
            wenzel_hess_dynamic_max.append(wenzel_times_hess_dynamic[key][-1])
            us_max_grad.append(us_times_grad[key][-1])
            us_max_hess.append(us_times_hess[key][-1])
    print(num_params_set)
    num_params_list = list(sorted(num_params_set))
    return wenzel_times_grad_static, wenzel_times_grad_dynamic, wenzel_times_hess_static, \
        wenzel_times_hess_dynamic, us_times_grad, us_times_hess, \
        functions, num_params_list, wenzel_grad_static_max, wenzel_grad_dynamic_max, \
        wenzel_hess_static_max, wenzel_hess_dynamic_max, us_max_grad, us_max_hess

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
    plt.savefig('./tests/results/hess/graphs/graph_{}_{}.png'.format(label, num_vars))
    plt.clf()

def generate_full_graph(avg_us_grad, avg_wenzel_grad_static, avg_wenzel_grad_dynamic, avg_us_hess, avg_wenzel_hess_static, avg_wenzel_hess_dynamic, denom, function, label, num_vars):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(denom, avg_us_grad,
             denom, avg_wenzel_grad_static,
             denom, avg_wenzel_grad_dynamic,
             denom, avg_us_hess,
             denom, avg_wenzel_hess_static,
             denom, avg_wenzel_hess_dynamic)
    # plt.xticks(denom)
    plt.title('Us Grad vs Mitsuba Grad (Static) vs. Mitsuba Grad (Dynamic) vs Us Hess vs Mitsuba Hess (Static) vs. Mitsuba Hess (Dynamic) # It: 10')
    # legend
    plt.legend( ('Us Grad', 'Mitsuba Grad (Static)', 'Mitsuba Grad (Dynamic)', 'Us Hess', 'Mitsuba Hess (Static)', 'Mitsuba Hess (Dynamic)'),
            shadow=True, loc=(0.01, 0.48), handlelength=1.5, fontsize=6)
    plt.xlabel('# params')
    plt.ylabel('time (s)')
    # plt.tight_layout()
    plt.figtext(0.99, 0.01, "y={}".format(function), horizontalalignment='right', fontsize=5)
    plt.savefig('./tests/results/hess/graphs/graph_{}_full.png'.format(num_vars))
    plt.clf()

def generate_max_graph(max_us_grad, max_wenzel_grad_static, max_wenzel_grad_dynamic, max_us_hess, max_wenzel_hess_static, max_wenzel_hess_dynamic, denom):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(denom, max_us_grad,
             denom, max_wenzel_grad_static,
             denom, max_wenzel_grad_dynamic,
             denom, max_us_hess,
             denom, max_wenzel_hess_static,
             denom, max_wenzel_hess_dynamic)
    # plt.xticks(denom)
    plt.title('Us Grad vs Mitsuba Grad (Static) vs. Mitsuba Grad (Dynamic) vs Us Hess vs Mitsuba Hess (Static) vs. Mitsuba Hess (Dynamic) # It: 10', fontsize=6)
    # legend
    plt.legend( ('Us Grad', 'Mitsuba Grad (Static)', 'Mitsuba Grad (Dynamic)', 'Us Hess', 'Mitsuba Hess (Static)', 'Mitsuba Hess (Dynamic)'),
            shadow=True, loc=(0.01, 0.48), handlelength=1.5, fontsize=6)
    plt.xlabel('# variables')
    plt.ylabel('time (s)')
    # plt.tight_layout()
    plt.savefig('./tests/results/hess/graphs/graph_max_full.png')
    plt.clf()

wenzel_times_grad_static, wenzel_times_grad_dynamic, wenzel_times_hess_static, \
wenzel_times_hess_dynamic, us_times_grad, us_times_hess, functions, num_params, \
wenzel_grad_static_max, wenzel_grad_dynamic_max, wenzel_hess_static_max, \
wenzel_hess_dynamic_max, us_max_grad, us_max_hess = convert_files_to_lists("./tests/results/hess/full_results_hessian-gcc49.json")

# for i, label in enumerate(functions):
    # generate_two_graph(us_times_grad[label], wenzel_times_grad_static[label], num_params, label, 'Mitsuba Gradient (Static)', i)
    # generate_two_graph(us_times_grad[label], wenzel_times_grad_dynamic[label], num_params, label, 'Mitsuba Gradient (Dynamic)', i)
    # generate_two_graph(us_times_hess[label], wenzel_times_hess_static[label], num_params, label, 'Mitsuba Hessian (Static)', i)
    # generate_two_graph(us_times_hess[label], wenzel_times_hess_dynamic[label], num_params, label, 'Mitsuba Hessian (Dynamic)', i)
    # generate_full_graph(us_times_grad[label], wenzel_times_grad_static[label], wenzel_times_grad_dynamic[label], us_times_hess[label],
    # wenzel_times_hess_static[label], wenzel_times_hess_dynamic[label], num_params, label, 'Wenzel', i)

generate_max_graph(us_max_grad, wenzel_grad_static_max, wenzel_hess_dynamic_max, us_max_hess,
wenzel_grad_static_max, wenzel_hess_dynamic_max, range(19))
