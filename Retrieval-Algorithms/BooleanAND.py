# This program looks at the inverted index and the lexicon, tokenizes the query
# Returns the document numbers that match the terms found in the tokenized query.
# Input: latimes-index directory/file_path, query file and the output file name

import sys
import os
import Modules.Tokenizer as Tokenizer
import time
import gzip

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

internal_id = 0
id_to_doc_map = {}

# print('reading metadataMap')
with open(metadataMapFileSource, "r") as file:
    for z in file:
        z = z.strip()
        id_to_doc_map[internal_id] = z
        internal_id += 1

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

    # print('Check if the query has been tokenized correctly for alphanumerics')
    # print('Query: '+queries[key])
    # print(tokenizedQuery)

    results = []

    # Custom sorting function to sort by the length of subarrays
    def sort_by_length(arr):
        return len(arr)

    for token in tokenizedQuery:
        try:
            tokenID = lexicon[token]
            tempList = invIndex[tokenID]
            postingList = [int(x) for x in tempList.split()]
            results.append(postingList)
            results.sort(key=sort_by_length)
        except KeyError:
            print('Could not find anything for '+token)

    # Here I checked if the returned postinglists are in order of small to big
    # print('Check if postingLists are in ascending order')
    # print(results)

    def IntersectFirst(p1, p2):
        answer = []
        i = 0
        j = 0
        while i < len(p1) and j < len(p2):
            if p1[i] == p2[j]:
                answer.append(p1[i])
                i += 2
                j += 2
            elif p1[i] < p2[j]:
                i += 2
            else:
                j += 2
        return answer

    def IntersectSecond(p1, p2):
        answer = []
        i = 0
        j = 0
        while i < len(p1) and j < len(p2):
            if p1[i] == p2[j]:
                answer.append(p1[i])
                i += 1
                j += 2
            elif p1[i] < p2[j]:
                i += 1
            else:
                j += 2
        return answer

    if len(results) > 1:
        mergedList = IntersectFirst(results[0], results[1])
        if len(results) > 2:
            for pList in results[2:]:
                mergedList = IntersectSecond(mergedList, pList)
    elif len(results) == 1:
        # code from https://stackoverflow.com/questions/12433695/extract-elements-of-list-at-odd-positions
        mergedList = results[0][0::2]

    # Checked the returned list of
    # print('Returned doc internal_id using Intersection Merge')
    # print(mergedList)

    score = len(mergedList)

    rank = 1
    for doc in mergedList:
        tempArr = [topicID, 'Q0', id_to_doc_map[doc],
                   rank, score-rank, 'sarengAND']
        output.append(tempArr)
        rank += 1

    mergedList = []

# print('Final Output as array of arrays')
# print(output)

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
