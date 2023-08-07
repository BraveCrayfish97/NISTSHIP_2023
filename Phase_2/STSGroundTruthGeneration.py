import os
import time
from requests import get
import sys

#ARGS
ground_truth_folder = sys.argv[1]
runs_folder = sys.argv[2]



print(runs_folder)
print(ground_truth_folder)

sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity"

def sss(s1, s2):
    try:

        response = get(sss_url, params={'operation':'api','phrase1':s1,'phrase2':s2}, headers={"user-agent":"NIST - TRECVID"})
        return float(response.text.strip())
    except:
        print ('Error in getting similarity for %s: %s' % ((s1,s2), response))
        return 0.0


#get list of gtruth files
gtruth_files = os.listdir(ground_truth_folder)

with open(f'GT_Output\\NewGroundTruth.txt', 'w') as data_file:
    
    i = 1
   
    for runs_file in os.listdir(runs_folder): ##** for ELT AND WASABI SPLIT BY TAB ELSE " "
        print("Now looking at " + runs_file)
        with open(f"{runs_folder}\\{runs_file}", "r") as file, open(f'GT_Output\\ThresholdData.txt','r') as t_file,  open(f"{ground_truth_folder}\\{gtruth_files[0]}", 'r') as gtruth_file_0,open(f"{ground_truth_folder}\\{gtruth_files[1]}", 'r') as gtruth_file_1,open(f"{ground_truth_folder}\\{gtruth_files[2]}", 'r') as gtruth_file_2,open(f"{ground_truth_folder}\\{gtruth_files[3]}", 'r') as gtruth_file_3,open(f"{ground_truth_folder}\\{gtruth_files[4]}", 'r') as gtruth_file_4:
            #data_file.write(f"{runs_file} NEW GT\n")
            file.readline()#skip first 3 lines of run file
            file.readline()
            file.readline()
            t_file.readline()#skip first line of threshold file
            for i in range(1, 6):#just doing first (6-1)->5 video IDs
                #extract runs data
                #* for ELT- and WASEDA make " " -> "\t" bcuz they use tabs in their run file
                line = file.readline()

                if "ELT" in runs_file or "Waseda" in runs_file:
                    first_space = line.index("\t")
                    second_space = line.find("\t", first_space+ 4)
                else:
                    first_space = line.index(" ")
                    second_space = line.find(" ", first_space+ 4)

                video_id = int(line[  0:first_space ])
                run_str = line[  second_space +1: len(line)    ]

                #extract groundtruth data from ALL 5 STS
                line = gtruth_file_0.readline()
                gtruth_str_0 = line[  line.index(" ") +1: len(line)    ]
                line = gtruth_file_1.readline()
                gtruth_str_1 = line[  line.index(" ") +1: len(line)    ]
                line = gtruth_file_2.readline()
                gtruth_str_2 = line[  line.index(" ") +1: len(line)    ]
                line = gtruth_file_3.readline()
                gtruth_str_3 = line[  line.index(" ") +1: len(line)    ]
                line = gtruth_file_4.readline()
                gtruth_str_4 = line[  line.index(" ") +1: len(line)    ]
                
                #write to NewGROUNDTRUTH if its ahbove the threshold for a given VIDEO ID
                

                               
                threshold = float(t_file.readline().split()[1])
                ####
                ###sts0 = sss(run_str, gtruth_str_0)
                ###data_file.write(f'{run_str} vs. {gtruth_str_0}')
                ###data_file.write(f'{i} {sts0}>{threshold} {run_str}\n')
                #########
                time.sleep(2)
                sts0 = sss(run_str, gtruth_str_0)
                if float(sts0) > threshold:
                    data_file.write(f'{i} {sts0}>{threshold} {run_str}\n')
                    continue
                
                time.sleep(2)
                sts1 = sss(run_str, gtruth_str_1)
                if float(sts1) > threshold:
                    data_file.write(f'{i} {sts1}>{threshold} {run_str}\n')
                    continue
                
                time.sleep(2)
                sts2 = sss(run_str, gtruth_str_2)
                if float(sts2) > threshold:
                    data_file.write(f'{i} {sts2}>{threshold} {run_str}\n')
                    continue
               
                time.sleep(2)
                sts3 = sss(run_str, gtruth_str_3)
                if float(sts3) > threshold:
                    data_file.write(f'{i} {sts3}>{threshold} {run_str}\n')
                    continue
                
                time.sleep(2)
                sts4 = sss(run_str, gtruth_str_4)
                if float(sts4) > threshold:
                    data_file.write(f'{i} {sts4}>{threshold} {run_str}\n')
                    continue
                
        """if float(sss(run_str, gtruth_str_1)) > threshold:
                    data_file.write(f'{sss(run_str, gtruth_str_1)} {gtruth_str_1}\n')
                #time.sleep(2)
                if float(sss(run_str, gtruth_str_2)) > threshold:
                    data_file.write(f'{sss(run_str, gtruth_str_2)} {gtruth_str_2}\n')
                #time.sleep(2)
                if float(sss(run_str, gtruth_str_3)) > threshold:
                    data_file.write(f'{sss(run_str, gtruth_str_3)} {gtruth_str_3}\n')
                #time.sleep(2)
                if float(sss(run_str, gtruth_str_4)) > threshold:
                    data_file.write(f'{sss(run_str, gtruth_str_4)} {gtruth_str_4}\n')
                #time.sleep(2)  """    