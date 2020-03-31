import matplotlib.pyplot as plt
import numpy as np
import os
import json
import seaborn as sns
import re

sns.set(style="darkgrid")


keys = ["./tests/complex/hess/3D_P1_non_zero", "./tests/complex/hess/3D_P2_non_zero", "./tests/complex/hess/3D_P2_zero", "./tests/complex/hess/3D_P3_non_zero",
         "./tests/complex/hess/3D_P4_non_zero"]

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def convertListToDict(file_list):
    with open("./tests/complex/wenzel/final_results.json") as wenzel_json:
        wenzel_data = json.load(wenzel_json)

    compile_map = {}
    static_speedup_map = {}
    dynamic_speedup_map = {}

    us_by_16_lines = []
    wenzel_dynamic = []
    wenzel_static = []
    static_16_speedup = []
    dyanmic_16_speedup = []

    for key in keys:
        compile_map[key] = []
        static_speedup_map[key] = []
        dynamic_speedup_map[key] = []
    for file_name in file_list:
        num_lines_index = file_name.rindex("_")
        last_period_index = file_name.rindex(".")
        num_lines = int(file_name[num_lines_index+1:last_period_index])
        print(num_lines)
        if num_lines <= 128:
            with open(file_name) as json_file:
                data = json.load(json_file)
                index_of_underscore = file_name.rindex("/")
                key = file_name[0:index_of_underscore]

                compile_map[key].append(data['total_compile_time'])

                index_of_last_underscore = key.rindex("/")
                wenzel_key = key[index_of_last_underscore+1:]

                wenzel_runtime_static = wenzel_data[wenzel_key]['avg_runtime_static']
                static_speedup = wenzel_runtime_static / float(data['avg_runtime'])
                static_speedup_map[key].append(static_speedup)

                wenzel_runtime_dynamic = wenzel_data[wenzel_key]['avg_runtime_dynamic']
                dynamic_speedup = wenzel_runtime_dynamic / float(data['avg_runtime'])
                dynamic_speedup_map[key].append(dynamic_speedup)

                print("Key: {}, Num_Lines: {}, Wenzel Runtime Static: {}, Static Speedup: {}, Wenzel Runtime Dynamic: {}, Dynamic Speedup: {}".format(
                    key, num_lines, wenzel_runtime_static, static_speedup, wenzel_runtime_dynamic, dynamic_speedup
                ))

                if num_lines == 128:
                    us_by_16_lines.append( float(data['avg_runtime']))
                    wenzel_static.append(wenzel_runtime_static)
                    wenzel_dynamic.append(wenzel_runtime_dynamic)
                    static_16_speedup.append(static_speedup)
                    dyanmic_16_speedup.append(dynamic_speedup)

    return static_speedup_map, dynamic_speedup_map, compile_map, us_by_16_lines, wenzel_dynamic, wenzel_static, \
        static_16_speedup, dyanmic_16_speedup

def generate_two_graph(avg_us, denom, title, label, static_or_dynamic, ylabel):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(denom, avg_us, '-bo')
    plt.title(title)
    plt.xlabel('Lines per File')
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig('./tests/complex/graphs/graph_{}_{}.png'.format(label, static_or_dynamic))
    plt.clf()

def generate_final_graph(us, them_static, them_dynamic, denom):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(denom, us, '-bo',
             denom, them_static, '-go',
             denom, them_dynamic, '-ro')
    # plt.xticks(denom)
    plt.title('Us vs Mitsuba (Static) vs Mitsuba (Dynamic) # It: 10, 128 Lines Per File', fontsize=10)
    # legend
    plt.legend( ('Ours', 'Mitsuba (Static)', 'Mitusba (Dynamic)'),
            shadow=True, loc=(0.01, 0.48), handlelength=1.5, fontsize=10)
    plt.xlabel('# vars')
    plt.ylabel('time (s)')
    plt.tight_layout()
    plt.savefig('./tests/complex/graphs/graph_by_128.png')
    plt.clf()

def generate_final_speedup_graph(them_static, them_dynamic, denom):
    # plt.figure(1)
    # plt.subplot(211)
    plt.plot(denom, them_static, color='#1abc9c', linestyle='dashed',  markersize=7)
    plt.plot(denom, them_dynamic, color='#f1c40f', linestyle='dashed', markersize=7)
    # legend
    plt.xlabel('Variables', fontfamily='monospace')
    plt.ylabel('Speedup', fontfamily='monospace')
    plt.legend( ('Mitsuba (Static)', 'Mitusba (Dynamic)'),
            shadow=False, fontsize=10, frameon=False)
    plt.margins(0,0)
    plt.savefig("./tests/complex/graphs/test_filename.pdf", bbox_inches = 'tight',
        pad_inches = 0)
    # plt.savefig('./tests/complex/graphs/graph_by_128_speedup.pdf')
    plt.clf()
    

directory = "./tests/complex/hess/"
file_list = []
for root, subdirs, files in os.walk(directory):
    for filename in files:
        file_path = os.path.join(root, filename)
        if ".json" in file_path:
            file_list.append(file_path)

file_list.sort(key=natural_keys)
print(file_list)

static_speedup_map, dynamic_speedup_map, compile_map, us_by_16_lines, wenzel_static, wenzel_dynamic, static_16_speedup, dyanmic_16_speedup = convertListToDict(file_list)

denom = [1, 2, 4, 8, 16, 32, 64, 128]

print("Static 16 Speedup: {}".format(static_16_speedup))

# for i, key in enumerate(keys):
#     print(key)
#     index_of_last_underscore = key.rindex("/") + 1
#     label = key[index_of_last_underscore:]
#     generate_two_graph(static_speedup_map[key], denom, 'Speedup of Static {}'.format(label), label, "static", "% Speedup")
#     generate_two_graph(dynamic_speedup_map[key], denom, 'Speedup of Dynamic {}'.format(label), label, "dynamic", "% Speedup")
#     generate_two_graph(compile_map[key], denom, 'Compilation', label, "compile", "time (s)")

# fig, axs = plt.subplots(5, 3)
# fig.tight_layout()
# for i, key in enumerate(keys):
#     if key != "./tests/complex/hess/3D_P4_non_zero":
#         print(key)
#         index_of_last_underscore = key.rindex("/") + 1
#         label = key[index_of_last_underscore:]
#         axs[i, 0].plot(denom, static_speedup_map[key])
#         axs[i, 0].set_title('Speedup of Static {}'.format(label), fontsize=6)
#         axs[i, 1].plot(denom, dynamic_speedup_map[key])
#         axs[i, 1].set_title('Speedup of Dynamic {}'.format(label), fontsize=6)
#         axs[i, 2].plot(denom, compile_map[key])
#         axs[i, 2].set_title('Compilation of {}'.format(label), fontsize=6)
# axs[4, 1].plot(denom, static_speedup_map['./tests/complex/hess/3D_P4_non_zero'])
# axs[4, 1].set_title('Speedup of 3D_P4_non_zero', fontsize=6)
# axs[4, 2].plot(denom, compile_map['./tests/complex/hess/3D_P4_non_zero'])
# axs[4, 2].set_title('Compilation of 3D_P4_non_zero', fontsize=6)
# plt.savefig('./tests/complex/graphs/same_graph.png')
# plt.clf()

denom = [12, 30, 30, 60, 105]
generate_final_graph(us_by_16_lines, wenzel_static, wenzel_dynamic, denom)
generate_final_speedup_graph(static_16_speedup, dyanmic_16_speedup, denom)