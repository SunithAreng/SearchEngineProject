# This program perfroms BM25 Retrieval
# This program looks at the inverted index, the lexicon and docLength, tokenizes the query
# Returns the document numbers are simliar to the terms found in the tokenized query.
# Input: latimes-index directory/file_path, query file and the output file name

import sys
import os
import Modules.Tokenizer as Tokenizer
import time
import gzip
import math
import operator

start_time = time.time()

inputLength = len(sys.argv)

b = 0.75
k_1 = 1.2
runtag = 'sarengBM25noStem'

# Get the current directory path
current_directory = os.getcwd()

# Checking if the argument conditions are satisfied
if inputLength == 4:
    fileSource = sys.argv[1]
    queryFileName = sys.argv[2]
    outputName = sys.argv[3]
else:
    if inputLength < 4:
        print("Too few Arguments!")
        print('Correct inputs are directory location of the index, queryfile_name.txt and output_filename.txt')
    else:
        print("Too many arguments!")
        print('Correct inputs are directory location of the index, queryfile_name.txt and output_filename.txt')
    sys.exit()

if not os.path.exists(fileSource):
    print("This file path does not exist. Please revise your input!")
    print('Please make sure to input the correct path.')
    sys.exit()

# File source for the metadata assuming IndexEngine has been run
metadataMapFileSource = fileSource+"/metadata/documentMap.txt"
invIndexFile = fileSource+"/metadata/invIndex.gz"
lexiconFile = fileSource+"/metadata/lexicon.txt"
docLengthFile = fileSource+"/metadata/doc-Length.txt"

internal_id = 0
id_to_doc_map = {}

# print('reading metadataMap')
with open(metadataMapFileSource, "r") as file:
    for z in file:
        z = z.strip()
        id_to_doc_map[internal_id] = z
        internal_id += 1

N = internal_id

# Creating Lexicon in memory
lexicon = {}
termId = 1
# print('reading lexicon')
with open(lexiconFile, "r") as file1:
    for z in file1:
        z = z.strip()
        lexicon[z] = termId
        termId += 1

# Creating Inverted Index in memory
invIndex = {}
termId = 1
# print('reading invIndex')
with gzip.open(invIndexFile, "rt") as file2:
    for z in file2:
        postingListString = z.strip()
        invIndex[termId] = postingListString
        termId += 1

# Reading Document Length File For Length Normalization Calc
internal_id = 0 
sum_length = 0
doc_Length = {}
with open(docLengthFile, "r") as file3:
    for z in file3:
        z = int(z.strip())
        sum_length += z
        doc_Length[internal_id] = z
        internal_id += 1

avdl = sum_length/N

queryFile = current_directory+'/'+queryFileName
outputFile = current_directory+'/'+outputName

# Code from https://stackoverflow.com/questions/35917558/read-two-consecutive-lines-from-a-file-into-a-dictionary-as-value-key-pairs
try:
    with open(queryFile) as f:
        queries = {int(id.strip()): query.strip() for id, query in zip(f, f)}
except FileNotFoundError:
    print('Query File does not exist!')
    print('Please make sure the query_file exists in the root directory.')
    sys.exit()

output = []

print('Retrieval in prgress!')
for key in queries:
    topicID = key
    tokenizedQuery = Tokenizer.Tokenize(queries[key])
    results = []
    
    for token in tokenizedQuery:
        try:
            tokenID = lexicon[token]
            tempList = invIndex[tokenID]
            postingList = [int(x) for x in tempList.split()]
            results.append(postingList)
       
        except KeyError:
            print('Could not find anything for '+token)

    BM_results = {}

    # BM25 score calculation
    for list_i in results:
        # Because a posting list contains docno-count pair
        # Division by 2 gives the total number of docs with that term
        n_i = len(list_i)/2 
        doc_pointer = 0
        tf_pointer = 1
        sx = (N-n_i+0.5)/(n_i+0.5)
        idf = math.log(sx)

        while doc_pointer < len(list_i):
            f_i = list_i[tf_pointer]   # Term Frequency from the array
            doc_id = list_i[doc_pointer]  # Docno from the array
            dl = doc_Length[doc_id]    # Retrieve Document length

            K = k_1*((1-b) + b*(dl/avdl))

            tf = f_i/(K+f_i)
            score = tf*idf

            if doc_id in BM_results:
                BM_results[doc_id] = BM_results[doc_id] + score
            else:
                BM_results[doc_id] = score

            doc_pointer +=2
            tf_pointer +=2
    
    # Code from https://ioflood.com/blog/python-sort-dictionary-by-value/#:~:text=To%20sort%20a%20dictionary%20by,itemgetter(1)))%20.
    sorted_BM25 = dict(sorted(BM_results.items(), key=operator.itemgetter(1), reverse=True))

    rank = 1
    for doc in sorted_BM25:
        tempArr = [topicID, 'Q0', id_to_doc_map[doc],
                   rank, sorted_BM25[doc], runtag]
        output.append(tempArr)

        if rank == 1000:
            break
        else:
            rank += 1

# The following code has been generated using ChatGPT
# the code tries to convert the inverted index of array of arrays into text file
with open(outputFile, 'w') as file:
    # Write each sub-array as a line
    for sub_array in output:
        # Convert the sub-array to a space-separated string
        line = " ".join(map(str, sub_array))
        file.write(line + "\n")

# Record end time
end_time = time.time()
elapsed_Time = round(end_time - start_time, 2)
print(f"Retrieval Complete! Duration: {elapsed_Time} seconds!")
