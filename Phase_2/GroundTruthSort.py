import os
import sys

#ARGs
gtruth_folder = sys.argv[1]

for file in os.listdir(f"{gtruth_folder}"):

    #make dict to store all 2008 vids, key - #, val - str
    ground_truth_data = {}
    with open(f"{gtruth_folder}\\{file}", 'r') as curr_file:
        for line in curr_file:
            video_id = int(line[  0:line.index(" ") ])
            ground_truth_data[video_id] = line[  line.index(" ") +1: len(line)    ]
    ground_truth_data = dict(sorted(ground_truth_data.items()))

    #rewrite file
    with open(f"{gtruth_folder}\\{file}", 'w') as curr_file:

        for key, val in ground_truth_data.items():
            curr_file.write(f'{key} {val}')
    
    
