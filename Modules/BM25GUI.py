# This program perfroms BM25 Retrieval
# This program looks at the inverted index, the lexicon and docLength, tokenizes the query
# Returns the document numbers are simliar to the terms found in the tokenized query.
# Used as a module for Interactive Search Engine

import Modules.Tokenizer as Tokenizer
import gzip
import math
import operator

def invIndexLoading(fileLocation):
    fileSource = fileLocation

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

    return N, avdl, lexicon, invIndex, id_to_doc_map, doc_Length

def BM25_Retrieval(query, input):
    N = input[0]
    avdl = input[1]
    lexicon = input[2]
    invIndex = input[3]
    id_to_doc_map = input[4]
    doc_Length = input[5]

    b = 0.75
    k_1 = 1.2
    
    output = {}

    tokenizedQuery = Tokenizer.Tokenize(query)
    results = []
    
    # Obtain PostingLists for the query tokens
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
        output[rank] = id_to_doc_map[doc]

        if rank == 10:
            break
        else:
            rank += 1

    return output
