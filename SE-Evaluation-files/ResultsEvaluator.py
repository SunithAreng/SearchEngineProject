# This program takes in the qrels file as 1st input and the a TREC results file as the 2nd input.
# This program then calculates Average Precision, NDCG@10, NDCG@1000 and Precision@10 for the given
# results file in a folder called 'Evaluated_Results'.

import sys
import os
from Modules.parsers import QrelsParser, ResultsParser
import time
import math

start_time = time.time()

inputLength = len(sys.argv)
current_directory = os.getcwd()

# Checking if the argument conditions are satisfied
if inputLength == 3:
    qrel_file = sys.argv[1]
    results_file = sys.argv[2]

    # Testing: comment this out later
    # qrel_file = current_directory+"/qrels/"+qrel_file
    # results_file = current_directory+"/results-files/"+results_file

else:
    if inputLength < 3:
        print("Too few Arguments!")
    else:
        print("Too many arguments!")
    sys.exit()

qrel = QrelsParser(qrel_file).parse()
try:
    result_parsed = ResultsParser(results_file).parse()
except Exception as e:
    print(
        f"Error producing results measures file with '{results_file}': {e}. Bad format. No Output was produced!")
    sys.exit()

results = result_parsed[1]
name = result_parsed[0]

output_path = current_directory+"/Evaluated_Results"
if not os.path.exists(output_path):
    os.mkdir(output_path)

output_file = output_path+"/"+name+"-measures.txt"

rel_docs = qrel.query_2_reldoc_nos
summary = []

for id in qrel.get_query_ids():
    results_count = 0
    recall = len(rel_docs[id])
    rel_doc_count = 0
    relvance = 0
    ap = 0
    p_10 = 0
    dcg_k = 0
    idcg_k = 0
    ndcg_10 = 0
    ndcg_1000 = 0
    precision_N = 0
    ndcg = 0

    for l in results.query_2_results[id]:
        results_count += 1
        if l.doc_id in rel_docs[id]:
            rel_doc_count += 1
            relvance = 1
        else:
            relvance = 0

        precision_N = rel_doc_count/results_count

        ap = ap + (1/recall)*relvance*precision_N

        dcg_k = dcg_k + (relvance)/(math.log2(results_count+1))

        if results_count <= recall:
            idcg_k = idcg_k + 1/(math.log2(results_count+1))

        ndcg = dcg_k/idcg_k

        if results_count == 10:
            p_10 = precision_N
            ndcg_10 = ndcg

        if results_count == 1000:
            ndcg_1000 = ndcg

    # The following covers some edge cases where the returned results
    # may be less than the cuts. In such cases, the final value of
    # of the measures are being used.
    if results_count < 1000:
        ndcg_1000 = ndcg

    if results_count < 10:
        p_10 = rel_doc_count/10
        ndcg_10 = ndcg

    # Formatting idea from
    # https://stackoverflow.com/questions/6149006/how-to-display-a-float-with-two-decimal-places

    temp_ap = ['ap', id, "{:.4f}".format(ap)]
    temp_p10 = ['P_10', id, "{:.4f}".format(p_10)]
    temp_ndcg10 = ['ndcg_cut_10', id, "{:.4f}".format(ndcg_10)]
    temp_ndcg1000 = ['ndcg_cut_1000', id, "{:.4f}".format(ndcg_1000)]
    summary.append(temp_ap)
    summary.append(temp_p10)
    summary.append(temp_ndcg10)
    summary.append(temp_ndcg1000)

# Code from https://stackoverflow.com/questions/4174941/how-to-sort-a-list-of-lists-by-a-specific-index-of-the-inner-list
summary.sort(key=lambda x: x[0].lower())

# Code taken from IndexEngine Program
with open(output_file, 'w') as file:
    # Write each sub-array as a line
    for sub_array in summary:
        # Convert the sub-array to a space-separated string
        line = " ".join(map(str, sub_array))
        file.write(line + "\n")

end_time = time.time()
elapsed_Time = round(end_time - start_time, 2)
print(f"Completed within {elapsed_Time} seconds!")
