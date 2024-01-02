# This program performs Cosine Similarity Retrieval
# It looks at the inverted index, lexicon and normalized docLength, tokenizes the query
# Returns the document numbers whose contents are most simliar to tokenized query.
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
docLengthNormFile = fileSource+"/metadata/doc-Length-Norm.txt"

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

# Reading Normalized Document length in memory
# This has been pre-computed at Index Engine
# The actual code can be found under DocLengthNormalization function in Tokenizer modoule
internal_id = 0 
doc_LengthNorm = {}
with open(docLengthNormFile, "r") as file3:
    for z in file3:
        z = float(z.strip())
        doc_LengthNorm[internal_id] = z
        internal_id += 1


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

    Cosine_results = {}

    # Cosine Similarity score calculation
    for list_i in results:
        # Because a posting list contains docno-count pair
        # Division by 2 gives the total number of docs with that term
        n_i = len(list_i)/2 
        doc_pointer = 0
        tf_pointer = 1
        sx = 1+(N/n_i)
        idf = math.log(sx)

        while doc_pointer < len(list_i):
            f_i = list_i[tf_pointer]
            doc_id = list_i[doc_pointer]
            dln = doc_LengthNorm[doc_id] #Retrieve the Norm DocLength

            # Calculate TF and IDF
            tf = 1+math.log(f_i)
            score = (1/dln)*tf*idf

            if doc_id in Cosine_results:
                Cosine_results[doc_id] = Cosine_results[doc_id] + score
            else:
                Cosine_results[doc_id] = score

            doc_pointer +=2
            tf_pointer +=2
    
    # Code from https://ioflood.com/blog/python-sort-dictionary-by-value/#:~:text=To%20sort%20a%20dictionary%20by,itemgetter(1)))%20.
    sorted_Cosine = dict(sorted(Cosine_results.items(), key=operator.itemgetter(1), reverse=True))

    rank = 1
    for doc in sorted_Cosine:
        tempArr = [topicID, 'Q0', id_to_doc_map[doc],
                   rank, sorted_Cosine[doc], 'sarengCosineNoStem']
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
