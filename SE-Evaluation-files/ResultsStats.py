# This program calculates the averages for each of the effectiveness measures
# from the output of each of the results files produced by ResultsEvaluator.py.
# Then stores them in one consolidated text file 'stats.txt' for analysis.

import os
import pandas as pd

current_directory = os.getcwd()
results_directory = current_directory+"/Evaluated_Results"

files = os.listdir(results_directory)

fileList = []
for file in files:
    if file.__contains__('sareng'):
        fileList.append(file)
    else:
        if file.__contains__('measure'):
            sep = file

# fileList.sort(key=lambda x: int(x.split('-')[0][7:]))

# fileList.append(sep)

output = [['Run_Name', 'Mean_Average_Precision',
           'Mean_P@10', 'Mean_NDCG@10', 'Mean_NDCG@1000']]

for f in fileList:

    name = f.split('-')[0]
    file = results_directory+'/'+f

    outputHeader = ['measure', 'topicID', 'score']
    df = pd.read_csv(file, sep=' ', names=outputHeader)

    ap_mean = df[df['measure'] == 'ap']['score'].mean()
    p10_mean = df[df['measure'] == 'P_10']['score'].mean()
    ndcg10_mean = df[df['measure'] == 'ndcg_cut_10']['score'].mean()
    ndcg1000_mean = df[df['measure'] == 'ndcg_cut_1000']['score'].mean()

    temp = [name, "{:.3f}".format(ap_mean), "{:.3f}".format(
        p10_mean), "{:.3f}".format(ndcg10_mean), "{:.3f}".format(ndcg1000_mean)]
    output.append(temp)

output_file = current_directory+'/stats.txt'

# Copied from IndexEngine.py program.
with open(output_file, 'w') as file:
    # Write each sub-array as a line
    for sub_array in output:
        # Convert the sub-array to a space-separated string
        line = " ".join(map(str, sub_array))
        file.write(line + "\n")

print('Complete!')
