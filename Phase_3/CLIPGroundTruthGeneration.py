import torch
from transformers import CLIPModel, CLIPProcessor, CLIPTokenizerFast

import os
import time
from requests import get
import sys

#ARGS
ground_truth_folder = sys.argv[1]
runs_folder = sys.argv[2]



print(runs_folder)
print(ground_truth_folder)

# Load the CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "openai/clip-vit-base-patch32"

model = CLIPModel.from_pretrained(model_id).to(device)
tokenizer = CLIPTokenizerFast.from_pretrained(model_id)
processor = CLIPProcessor.from_pretrained(model_id)

total_IDs = 2008

#list to hold data for histogram
data=[]
#get list of gtruth files
gtruth_files = os.listdir(ground_truth_folder)

with open(f'GT_Output\\NewCLIPGroundTruth.txt', 'w') as data_file:
    
    i = 1
   
    for runs_file in os.listdir(runs_folder): ##** for ELT AND WASABI SPLIT BY TAB ELSE " "
        print("Now looking at " + runs_file)
        with open(f"{runs_folder}\\{runs_file}", "r") as file, open(f'GT_Output\\CLIPThresholdData.txt','r') as t_file,  open(f"{ground_truth_folder}\\{gtruth_files[0]}", 'r') as gtruth_file_0,open(f"{ground_truth_folder}\\{gtruth_files[1]}", 'r') as gtruth_file_1,open(f"{ground_truth_folder}\\{gtruth_files[2]}", 'r') as gtruth_file_2,open(f"{ground_truth_folder}\\{gtruth_files[3]}", 'r') as gtruth_file_3,open(f"{ground_truth_folder}\\{gtruth_files[4]}", 'r') as gtruth_file_4:
            #data_file.write(f"{runs_file} NEW GT\n")
            file.readline()#skip first 3 lines of run file
            file.readline()
            file.readline()
            t_file.readline()#skip first line of threshold file
            for i in range(1, total_IDs+1):#just doing first (6-1)->5 video IDs
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

                #time.sleep(2)
                text_input_1 = tokenizer(run_str, return_tensors="pt")
                text_input_2 = tokenizer(gtruth_str_0, return_tensors="pt")

                #CHATGPT SOL.
                # Check the length of tokenized inputs
                if len(text_input_1["input_ids"].flatten()) > 77 or len(text_input_2["input_ids"].flatten()) > 77:
                    print("Input text is too long, skipping.")
                    continue

                with torch.no_grad():
                    text_embedding_1 = model.get_text_features(**text_input_1)
                    text_embedding_2 = model.get_text_features(**text_input_2)
                # Compute the cosine similarity
                cossim0 = torch.nn.functional.cosine_similarity(text_embedding_1, text_embedding_2).item()
                
                if float(cossim0) > threshold:
                    data_file.write(f'{i} {cossim0}>{threshold} {run_str}vs{gtruth_str_0}\n')
                    continue


                #time.sleep(2)
                text_input_1 = tokenizer(run_str, return_tensors="pt")
                text_input_2 = tokenizer(gtruth_str_1, return_tensors="pt")
                #CHATGPT SOL.
                # Check the length of tokenized inputs
                if len(text_input_1["input_ids"].flatten()) > 77 or len(text_input_2["input_ids"].flatten()) > 77:
                    print("Input text is too long, skipping.")
                    continue

                with torch.no_grad():
                    text_embedding_1 = model.get_text_features(**text_input_1)
                    text_embedding_2 = model.get_text_features(**text_input_2)
                # Compute the cosine similarity
                cossim1 = torch.nn.functional.cosine_similarity(text_embedding_1, text_embedding_2).item()
                
                if float(cossim1) > threshold:
                    data_file.write(f'{i} {cossim1}>{threshold} {run_str}vs{gtruth_str_1}\n')
                    continue


                #time.sleep(2)
                text_input_1 = tokenizer(run_str, return_tensors="pt")
                text_input_2 = tokenizer(gtruth_str_2, return_tensors="pt")
                #CHATGPT SOL.
                # Check the length of tokenized inputs
                if len(text_input_1["input_ids"].flatten()) > 77 or len(text_input_2["input_ids"].flatten()) > 77:
                    print("Input text is too long, skipping.")
                    continue

                with torch.no_grad():
                    text_embedding_1 = model.get_text_features(**text_input_1)
                    text_embedding_2 = model.get_text_features(**text_input_2)
                # Compute the cosine similarity
                cossim2 = torch.nn.functional.cosine_similarity(text_embedding_1, text_embedding_2).item()
                
                if float(cossim2) > threshold:
                    data_file.write(f'{i} {cossim2}>{threshold} {run_str}vs{gtruth_str_2}\n')
                    continue


                #time.sleep(2)
                text_input_1 = tokenizer(run_str, return_tensors="pt")
                text_input_2 = tokenizer(gtruth_str_3, return_tensors="pt")
                #CHATGPT SOL.
                # Check the length of tokenized inputs
                if len(text_input_1["input_ids"].flatten()) > 77 or len(text_input_2["input_ids"].flatten()) > 77:
                    print("Input text is too long, skipping.")
                    continue

                with torch.no_grad():
                    text_embedding_1 = model.get_text_features(**text_input_1)
                    text_embedding_2 = model.get_text_features(**text_input_2)
                # Compute the cosine similarity
                cossim3 = torch.nn.functional.cosine_similarity(text_embedding_1, text_embedding_2).item()
                
                if float(cossim3) > threshold:
                    data_file.write(f'{i} {cossim3}>{threshold} {run_str}vs{gtruth_str_3}\n')
                    continue
                

                #time.sleep(2)
                text_input_1 = tokenizer(run_str, return_tensors="pt")
                text_input_2 = tokenizer(gtruth_str_4, return_tensors="pt")
                #CHATGPT SOL.
                # Check the length of tokenized inputs
                if len(text_input_1["input_ids"].flatten()) > 77 or len(text_input_2["input_ids"].flatten()) > 77:
                    print("Input text is too long, skipping.")
                    continue

                with torch.no_grad():
                    text_embedding_1 = model.get_text_features(**text_input_1)
                    text_embedding_2 = model.get_text_features(**text_input_2)
                # Compute the cosine similarity
                cossim4 = torch.nn.functional.cosine_similarity(text_embedding_1, text_embedding_2).item()
                
                if float(cossim4) > threshold:
                    data_file.write(f'{i} {cossim4}>{threshold} {run_str}vs{gtruth_str_4}\n')
                    continue
                
                """time.sleep(2)
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
                """