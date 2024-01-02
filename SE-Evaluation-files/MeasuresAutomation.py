# This is an automation file that takes automates creation of evaluated results files
# The program assumes that there is a folder called "results-files" which contains all
# the results and runs ResultsEvaluator.py program in loop for all the results files.
# The output is produced in another folder called "Evaluated_Results" which is created
# by the ResultsEvaluator.py program in the root directory during its run.

import os
import subprocess

current_directory = os.getcwd()
results_directory = current_directory+"/results-files"

files = os.listdir(results_directory)

fileList = []
for file in files:
    if file.__contains__('results'):
        fileList.append(file)

script_path = current_directory+'/ResultsEvaluator.py'

fileList.sort(reverse=True)

for measureFile in fileList:
    try:
        command = ["python3", script_path, 'qrels/qrels.txt',
                   results_directory+'/'+measureFile]
        subprocess.run(command)
    except Exception as e:
        print(f"There are some issues with {measureFile}: '{e}'")
