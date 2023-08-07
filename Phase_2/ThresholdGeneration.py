import os
import time
from requests import get
import sys
import numpy as np

#ARGS------
ground_truth_folder = sys.argv[1]

margin = 0.1
min_threshold = 0.6
#how many video IDs do you want to get the threshold for- if you want all- set equal to 2008
total_IDs = 5

sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity"
def sss(s1, s2):
    try:

        response = get(sss_url, params={'operation':'api','phrase1':s1,'phrase2':s2}, headers={"user-agent":"NIST-TRECVID"})
        return float(response.text.strip())
    except:
        print ('Error in getting similarity for %s: %s' % ((s1,s2), response))
        return 0.0

ground_truth_files = os.listdir(ground_truth_folder)

thresholds = np.ones(total_IDs)

#SET DEFAULT VALS FOR NP ARRAY TO 0.6 ********


for i in range(len(ground_truth_files)):
        for j in range(i + 1, len(ground_truth_files)):
            with open(f"{ground_truth_folder}/{ground_truth_files[i]}", 'r') as file1, open(f"{ground_truth_folder}/{ground_truth_files[j]}", 'r') as file2:
               print(f'Opening {ground_truth_files[i]}')
               print(f'Opening {ground_truth_files[j]}')
               for l in range(1, total_IDs+1):
                    line1 = file1.readline()
                    s1 = line1[line1.index(" ") + 1:].strip()
                    line2 = file2.readline()
                    s2 = line2[line2.index(" ") + 1:].strip()
                    sts = sss(s1, s2)
                    #print(f'{sts} {s1} vs.\n{s2}\n\n')
                    if sts<min_threshold-margin:
                        thresholds[l-1] = min_threshold-margin#cuz we will add margin later
                    elif thresholds[l-1]>sts:
                         thresholds[l-1] = sts
                    #time.sleep(2)
            file2.close()
            file1.close()
os.mkdir("GT_Output")
with open(f"GT_Output\\ThresholdData.txt", 'w') as file:
    file.write("ID   Threshold\n")
    
    for i in range(0, len(thresholds)):
        num_spaces = 12 - len(str(i)) - (2+5) #ID and 7 for threshold rounded to 5 places
        file.write(str(i+1)+(" " * num_spaces)+("{:.5f}".format(thresholds[i]+margin))+"\n")



