import os
import time
from requests import get
import sys
import numpy as np
import torch
from transformers import CLIPModel, CLIPProcessor, CLIPTokenizerFast
#ARGS------
ground_truth_folder = sys.argv[1]


# Load the CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "openai/clip-vit-base-patch32"

model = CLIPModel.from_pretrained(model_id).to(device)
tokenizer = CLIPTokenizerFast.from_pretrained(model_id)
processor = CLIPProcessor.from_pretrained(model_id)


margin = 0.15
min_threshold = 0.7
#how many video IDs do you want to get the threshold for- if you want all- set equal to 2008
total_IDs = 2008

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

                    text_input_1 = tokenizer(s1, return_tensors="pt")
                    text_input_2 = tokenizer(s2, return_tensors="pt")


                    #CHATGPT SOL.
                    # Check the length of tokenized inputs
                    if len(text_input_1["input_ids"].flatten()) > 77 or len(text_input_2["input_ids"].flatten()) > 77:
                        print("Input text is too long, skipping.")
                        continue

                    with torch.no_grad():
                        text_embedding_1 = model.get_text_features(**text_input_1)
                        text_embedding_2 = model.get_text_features(**text_input_2)
                    # Compute the cosine similarity
                    cossim = torch.nn.functional.cosine_similarity(text_embedding_1, text_embedding_2).item()

                    if cossim<min_threshold-margin:
                        thresholds[l-1] = min_threshold-margin#cuz we will add margin later
                    elif thresholds[l-1]>cossim:
                         thresholds[l-1] = cossim

            file2.close()
            file1.close()
os.mkdir("GT_Output")
with open(f"GT_Output\\CLIPThresholdData.txt", 'w') as file:
    file.write("ID   Threshold\n")
    
    for i in range(0, len(thresholds)):
        num_spaces = 12 - len(str(i)) - (2+5) #ID and 7 for threshold rounded to 5 places
        file.write(str(i+1)+(" " * num_spaces)+("{:.5f}".format(thresholds[i]+margin))+"\n")

