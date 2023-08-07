import matplotlib
import matplotlib.pyplot as plt
import sys
import os
import numpy

#----- args for this script
# 1- metric - not case sensitive
# 2- folder name containing metric data


metric = sys.argv[1].lower()
print(metric)

folder = sys.argv[2]

metrics = ["cider", "ciderD", "BLEU", "spice", "meteor"]
for metric in metrics:

    #look for ".metric." in file names
    temp =""
    files = os.listdir(folder)
    for metric_file in files:
        if f".{metric.lower()}." in metric_file.lower():
            temp = metric_file
    metric_file = temp
    #now file points to the correct metric file
        


    year = int(metric_file[2:4])
    final_file = f"tv{year}.FinalRankings.txt"

    #__METRIC__ VS FINAL


    metric_ranks = []
    final_ranks = []
    x_values = []

    #create final ranks list - index + 1 equals x val
    i=1
    with open(final_file, "r") as file:
        for line in file:
            run = line.split()
            final_ranks.append(run[0])
            x_values.append(i)
            i+=1
    print(final_ranks)
    print(x_values)
    print('\n\n\n\n')

    #create metric ranks list
    with open(f"{folder}\\{metric_file}", "r") as file:
        for line in file:
            print(line +"\n")
            run = line.split()
            if metric == "cider" or metric == "ciderD":
                metric_ranks.append(run[0][  8:len(run[0])-10 ])
            if metric == "meteor":
                metric_ranks.append(run[0][ 0:len(run[0])-13   ])
            else:
                metric_ranks.append(run[0])
            
    #match the x vals to the y vals
    y_values =[]
    print(f"{folder}\\{metric_file}")
    print(metric_ranks)
    for x in x_values:
        y_values.append(  metric_ranks.index(final_ranks[x-1])+1  )
    print(y_values)

    corr_matrix = numpy.corrcoef(x_values, y_values)
    corr = corr_matrix[0,1]
    R_sq = corr**2
    
    print(R_sq)
    # Create a scatter plot using the extracted coordinates
    plt.scatter(x_values, y_values)
    plt.annotate(f'R-squared = {R_sq:.4f}', xy=(0.05, 0.9), xycoords='axes fraction')
    # Set labels for x-axis and y-axis
    plt.xlabel('X')
    plt.ylabel('Y')

    # Set a title for the plot
    plt.title(f'{metric.upper()} VS FINAL')

    # Save the plot
    #Create dir unless already created
    save_folder = f'tv{year}_Output_Data'
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    plt.savefig(f'{save_folder}\\tv{year}.{metric.upper()}vsFINAL.png')
    plt.close()
print(year)


#-----------------------------------
#STS VS FINAL

#average the scores for each run and then rank based off that
sts_avg_scores = {}
#calc each runs avg score across 5 STS files
for j in range(1,6):
    
    file_path = f"RankingData\\tv{year}.vtt.sts.results.table.{j}.non_progress"  
    with open(file_path, "r") as file:
        for line in file:
            run = line.split()
            if j == 1:
                sts_avg_scores[run[0][ 0:len(run[0])-6   ]] = float(run[1])/5
            else:
                sts_avg_scores[run[0][ 0:len(run[0])-6   ]] += float(run[1])/5

#sort STS final ranking descending by val
sts_avg_scores = sorted(sts_avg_scores.items(), key=lambda x:x[1], reverse=True)
sts_ranks = []

print(sts_avg_scores)
#match the x vals to the y vals
for tup in sts_avg_scores:
    sts_ranks.append(tup[0])
y_values =[]
for x in x_values:
    y_values.append(  sts_ranks.index(final_ranks[x-1])+1  )
print(y_values)

 
corr_matrix = numpy.corrcoef(x_values, y_values)
corr = corr_matrix[0,1]
R_sq = corr**2
 
print(R_sq)




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



"""

#ORIGINAL CODE---------vv

year = int(metric_file[2:4])
final_file = f"tv{year}.FinalRankings.txt"

#__METRIC__ VS FINAL


metric_ranks = []
final_ranks = []
x_values = []

#create final ranks list - index + 1 equals x val
i=1
with open(final_file, "r") as file:
    for line in file:
        run = line.split()
        final_ranks.append(run[0])
        x_values.append(i)
        i+=1
print(final_ranks)
print(x_values)
print('\n\n\n\n')

#create metric ranks list
if metric != "sts":
    with open(f"{folder}\\{metric_file}", "r") as file:
        for line in file:
            print(line +"\n")
            run = line.split()
            if metric == "cider" or metric == "ciderd":
                metric_ranks.append(run[0][  8:len(run[0])-10 ])
            if metric == "meteor":
                metric_ranks.append(run[0][ 0:len(run[0])-13   ])
            else:
                metric_ranks.append(run[0])
            
    #match the x vals to the y vals
    y_values =[]
    print(f"{folder}\\{metric_file}")
    print(metric_ranks)
    for x in x_values:
        y_values.append(  metric_ranks.index(final_ranks[x-1])+1  )
    print(y_values)


else:
    #average the scores for each run and then rank based off that
    sts_avg_scores = {}

    #calc each runs avg score across 5 STS files
    for j in range(1,6):
        
        file_path = f"RankingData\\tv{year}.vtt.sts.results.table.{j}.non_progress"  

        with open(file_path, "r") as file:
            for line in file:
                run = line.split()
                if j == 1:
                    sts_avg_scores[run[0][ 0:len(run[0])-6   ]] = float(run[1])/5
                else:
                    sts_avg_scores[run[0][ 0:len(run[0])-6   ]] += float(run[1])/5

    #sort STS final ranking descending by val
    sts_avg_scores = sorted(sts_avg_scores.items(), key=lambda x:x[1], reverse=True)
    sts_ranks = []
    
    print(sts_avg_scores)
    #match the x vals to the y vals
    for tup in sts_avg_scores:
        sts_ranks.append(tup[0])
    y_values =[]
    for x in x_values:
        y_values.append(  sts_ranks.index(final_ranks[x-1])+1  )
    print(y_values)

 
corr_matrix = numpy.corrcoef(x_values, y_values)
corr = corr_matrix[0,1]
R_sq = corr**2
 
print(R_sq)




# Create a scatter plot using the extracted coordinates
plt.scatter(x_values, y_values)
plt.annotate(f'R-squared = {R_sq:.4f}', xy=(0.05, 0.9), xycoords='axes fraction')
# Set labels for x-axis and y-axis
plt.xlabel('X')
plt.ylabel('Y')

# Set a title for the plot
plt.title(f'{metric.upper()} VS FINAL')

# Display the plot
plt.show()



"""