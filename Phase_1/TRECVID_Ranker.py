import matplotlib.pyplot as plt
import sys
import os
import numpy






#**************
#for the 2018 spaces need to be reomved and reaplced with _
#for 2017 u have to delete "results"



#handle args
arguments = sys.argv

folder = sys.argv[1]
files = os.listdir(folder)
for file in files:
    pass

year = int(file[2:4])
save_folder = f'tv{year}_Output_Data'
os.mkdir(save_folder)

#make variables to account for data inconsistency
# for 2021 & 2022 it should be 13, for the rest is should be 21

if year >= 20:

    cider_front_offset = 8
    cider_offset = 10


    ciderD_front_offset = 8
    ciderD_offset = 10

    bleu_offset = 0
    sts_offset = 6
    if year == 20:
        meteor_offset = 21
    else:
        meteor_offset = 13
else:
    if year == 19:
        cider_front_offset = 2
        ciderD_front_offset = 2
    else:
        cider_front_offset = 0
        ciderD_front_offset = 0
    
    cider_offset = 0
    ciderD_offset = 0

    bleu_offset = 4
    sts_offset = 10
    meteor_offset = 25
  


#def regular_ranker vvvv - maybe make diff kinds

#CIDER
#ignore first 8 and last 10
run_scores = {}#since first one, make dict will all runs as key and sum as count
#get correct filepath
temp =""
files = os.listdir(folder)
for file_path in files:
    if f".cider." in file_path.lower():
        temp = file_path
file_path = f'{folder}\\{temp}'

i=0
with open(file_path, "r") as file:
    for line in file:
        run = line.split()
        run_scores[ run[0][  cider_front_offset:len(run[0])-cider_offset ] ] = i
        i += 1



#CIDERD
#ignore first 8 and last 10
#get correct filepath
temp =""
files = os.listdir(folder)
for file_path in files:
    if f".ciderd." in file_path.lower():
        temp = file_path
file_path = f'{folder}\\{temp}'

i=0
with open(file_path, "r") as file:
    for line in file:
        run = line.split()
        run_scores[ run[0][  ciderD_front_offset:len(run[0])-ciderD_offset ] ] += i
        i += 1

#SPICE
#get correct filepath
try:
    temp =""
    files = os.listdir(folder)
    for file_path in files:
        if f".spice." in file_path.lower():
            temp = file_path
    file_path = f'{folder}\\{temp}'

    i=0
    with open(file_path, "r") as file:
        for line in file:
            run = line.split()
            run_scores[run[0]] += i
            i += 1 
except Exception as e:
    print("no spice")


#BLEU
#get correct filepath
temp =""
files = os.listdir(folder)
for file_path in files:
    if f".bleu." in file_path.lower():
        temp = file_path
file_path = f'{folder}\\{temp}'

i=0
with open(file_path, "r") as file:
    for line in file:
        run = line.split()
        print(run)
        run_scores[run[0][  0:len(run[0])-bleu_offset   ]] += i
        i += 1


#METEOR
#get correct filepath
temp =""
files = os.listdir(folder)
for file_path in files:
    if f".meteor." in file_path.lower():
        temp = file_path
file_path = f'{folder}\\{temp}'

i=0
with open(file_path, "r") as file:
    for line in file:
        run = line.split()
        run_scores[run[0][ 0:len(run[0])- meteor_offset   ]] += i
        i += 1


#STS-5 files
#ignore last 5 characters

#average the scores for each run and then rank based off that
sts_avg_scores = {}

#calc each runs avg score across 5 STS files
for j in range(1,6):
    #get correct filepath
    temp =""
    files = os.listdir(folder)
    for file_path in files:
        if (f".sts." in file_path.lower()) and (f".{j}" in file_path.lower()):
            temp = file_path
    file_path = f'{folder}\\{temp}'

    i=0
    with open(file_path, "r") as file:
        for line in file:
            run = line.split()
            if j == 1:
                sts_avg_scores[run[0][ 0:len(run[0])-sts_offset   ]] = float(run[1])/5
            else:
                sts_avg_scores[run[0][ 0:len(run[0])-sts_offset   ]] += float(run[1])/5
            i += 1
#sort STS final ranking descending by val
sts_avg_scores = sorted(sts_avg_scores.items(), key=lambda x:x[1], reverse=True)

#add STS ranking to final ranking

i=0
for k in sts_avg_scores:
    run_scores[k[0]] += i
    i +=1
sorted_final = sorted(run_scores.items(), key=lambda x:x[1])

def format_line(run, number, filename):
    # Calculate the number of spaces needed between username and number
    num_spaces = 65 - len(run) - len(str(number))

    # Create the formatted line with username, spaces, and number
    line = f"{run}{' ' * num_spaces}{number}"

    with open(filename, 'a') as file:
        file.write(line + '\n')


filename = f"{save_folder}\\tv{year}.FinalRankings.txt"
for row in sorted_final:
    format_line(row[0], row[1], filename=filename)
    

# -------------------------
# METRIC COMPARISON
# VVVVVVVVVVVVVVVVVVVVVVVV

metrics = ["cider", "ciderd", "bleu", "spice", "meteor"]
for metric in metrics:

    #look for ".metric." in file names
    temp =""
    files = os.listdir(folder)
    for metric_file in files:
        if f".{metric.lower()}." in metric_file.lower():
            temp = metric_file
    metric_file = temp
    if metric_file =="":
        continue
    #now file points to the correct metric file
        


    final_file = f"tv{year}.FinalRankings.txt"

    #__METRIC__ VS FINAL


    metric_ranks = []
    final_ranks = []
    x_values = []

    #create final ranks list - index + 1 equals x val
    i=1
    with open(f'{save_folder}\\{final_file}', "r") as file:
        for line in file:
            run = line.split()
            final_ranks.append(run[0])
            x_values.append(i)
            i+=1


    #create metric ranks list
    with open(f"{folder}\\{metric_file}", "r") as file:
        for line in file:

            run = line.split()
            if metric == "cider":
                metric_ranks.append(run[0][  cider_front_offset:len(run[0])-cider_offset ])
            if metric == "ciderd":
                metric_ranks.append(run[0][  ciderD_front_offset:len(run[0])-ciderD_offset ])
            if metric == "bleu":
                metric_ranks.append(run[0][  0:len(run[0])-bleu_offset ])
            if metric == "meteor":
                metric_ranks.append(run[0][ 0:len(run[0])-meteor_offset   ])
            if metric == 'spice':
                metric_ranks.append(run[0] )
                
            
    #match the x vals to the y vals
    y_values =[]
    for x in x_values:
        y_values.append(  metric_ranks.index(final_ranks[x-1])+1  )

    corr_matrix = numpy.corrcoef(x_values, y_values)
    corr = corr_matrix[0,1]
    R_sq = corr**2
    
    #print R sq formatted
    num_spaces = 15 - len(metric) - 5

    # Create the formatted line with username, spaces, and number
    line = f"{metric}{' ' * num_spaces}{R_sq:.5f}"
    print(line)
    # Create a scatter plot using the extracted coordinates
    plt.scatter(x_values, y_values)
    plt.annotate(f'R-squared = {R_sq:.4f}', xy=(0.05, 0.9), xycoords='axes fraction')
    # Set labels for x-axis and y-axis
    plt.xlabel('X')
    plt.ylabel('Y')

    # Set a title for the plot
    plt.title(f'{metric.upper()} VS FINAL')

    # Save the plot
    
    plt.savefig(f'{save_folder}\\tv{year}.{metric.upper()}vsFINAL.png')
    plt.close()


#-----------------------------------
#STS VS FINAL

#average the scores for each run and then rank based off that
sts_avg_scores = {}
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
        for line in file:
            run = line.split()
            if j == 1:
                sts_avg_scores[run[0][ 0:len(run[0])-sts_offset   ]] = float(run[1])/5
            else:
                sts_avg_scores[run[0][ 0:len(run[0])-sts_offset   ]] += float(run[1])/5

#sort STS final ranking descending by val
sts_avg_scores = sorted(sts_avg_scores.items(), key=lambda x:x[1], reverse=True)
sts_ranks = []

#match the x vals to the y vals
for tup in sts_avg_scores:
    sts_ranks.append(tup[0])
y_values =[]
for x in x_values:
    y_values.append(  sts_ranks.index(final_ranks[x-1])+1  )

 
corr_matrix = numpy.corrcoef(x_values, y_values)
corr = corr_matrix[0,1]
R_sq = corr**2
 
#print R sq formatted
num_spaces = 15 - len("STS") - 5

# Create the formatted line with username, spaces, and number
line = f"STS{' ' * num_spaces}{R_sq:.5f}"
print(line)

# Create a scatter plot using the extracted coordinates
plt.scatter(x_values, y_values)
plt.annotate(f'R-squared = {R_sq:.4f}', xy=(0.05, 0.9), xycoords='axes fraction')
# Set labels for x-axis and y-axis
plt.xlabel('X')
plt.ylabel('Y')

# Set a title for the plot
plt.title('STS VS FINAL')

# Display the plot
plt.savefig(f'{save_folder}\\tv{year}.STSvsFINAL.png')
plt.close()

