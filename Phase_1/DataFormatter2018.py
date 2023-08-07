import matplotlib
import matplotlib.pyplot as plt
import sys
import os


#code to fix 2018
folder = "RankingData2018"
metrics = ["cider", "ciderD", "BLEU", "meteor"]
for metric in metrics:

    #look for ".metric." in file names
    temp =""
    files = os.listdir(folder)
    for metric_file in files:
        if f".{metric.lower()}." in metric_file.lower():
            temp = metric_file
    metric_file = temp
    #now file points to the correct metric file

    fix = False
    with open(f'{folder}\\{metric_file}', "r") as file:
        rewrite = ""
        for line in file:
            content = line.split()
            if len(content) == 3:
                fix = True
                # Calculate the number of spaces needed between username and number
                num_spaces = 90 - (len(content[1])+2) - len(content[2])

                # Create the formatted line with username, spaces, and number
                line = f"{content[0]}_{content[1]}{' ' * num_spaces}{content[2]}\n"
                rewrite = rewrite + line
    if fix:
        with open(f'{folder}\\{metric_file}', 'w') as file:
            file.write(rewrite + '\n')
                
    print("\n\n\n")





#calc each runs avg score across 5 STS files
for j in range(1,6):
    #get correct filepath
    temp =""
    files = os.listdir(folder)
    for file_path in files:
        if (f".sts." in file_path.lower()) and (f".{j}" in file_path.lower()):
            temp = file_path
    file_path = f'{folder}\\{temp}'

    with open(file_path, "r") as file:
        rewrite = ""
        for line in file:
            content = line.split()
            if len(content) == 3:
                fix = True
                # Calculate the number of spaces needed between username and number
                num_spaces = 75 - (len(content[1])+2) - len(content[2])

                # Create the formatted line with username, spaces, and number
                line = f"{content[0]}_{content[1]}{' ' * num_spaces}{content[2]}\n"
                rewrite = rewrite + line
    if fix:
        with open(file_path, 'w') as file:
            file.write(rewrite + '\n')











