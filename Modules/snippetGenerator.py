# This program is a helper module for SearchEngine Program
# It contains snippetGen function which has 4 arugments
# This script will create query-biased snippet for a single document 
# and return its output to its parent program

import Modules.MetaDataExtractor as MetaDataExtractor
import gzip
import xml.etree.ElementTree as ET
import Modules.Tokenizer as Tokenizer
import re
from heapq import heapify, heappop

def snippetGen(fileSource, rank, docno, query):
    
    date = MetaDataExtractor.parseDate(docno)
    tokenizedQuery = Tokenizer.Tokenize(query)
    docNumber = docno

    file = fileSource+"/docs/"+date['year']+"/" + \
        date['month']+"/"+date['day']+"/"+docNumber+".gz"
    
    metaDataFile = fileSource+"/docs/" + \
        date['year']+"/"+date['month']+"/" + \
        date['day']+"/"+docNumber+"-metadata.txt"

    metadataDict = {}
    with open(metaDataFile, "r") as mfile:
        for line in mfile:
            # Generated using ChatGPT
            # Split only on the first colon encountered
            key, value = map(str.strip, line.split(':', 1))
            metadataDict[key] = value
    
    with gzip.open(file, 'r') as f:
        content = f.read()
    
    root = ET.fromstring(content)

    # Find all 'P' elements and their text within the 'TEXT' tags
    text_elements = root.findall('.//TEXT/P')

    # Copied from https://stackoverflow.com/questions/14622835/split-string-on-or-keeping-the-punctuation-mark
    split_rules = re.compile(r'(?<=[.!?])')
    
    # Find all 'P' elements and their text within the 'GRAPHIC' tag
    graphic_elements = root.findall('.//GRAPHIC/P')
    
    text_elements.extend(graphic_elements)

    count = 0
    heap = [] 
    for textBody in text_elements:
        
        body= textBody.text.strip()
        body= body.replace('\n', ' ')
        tempArr = split_rules.split(body)

        # The following code removes the empty elements from the list
        # Copied from https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
        sentencesArray = list(filter(None, tempArr))
        
        header = False
        if len(sentencesArray) == 1:
            header = True  

        for sentence in sentencesArray:
            tokenizedSentence = Tokenizer.Tokenize(sentence)
            intersect = set(tokenizedQuery).intersection(tokenizedSentence)

            h = 0
            if header:
                h = 1
            
            temp = {}
            for x in tokenizedSentence:
                if x in temp:
                    temp[x] +=1
                else:
                    temp[x] = 0

            c = 0
            for token in tokenizedQuery:
                if token in temp:
                    c = c + temp[token]

            d = len(intersect)

            # The following 2 functions has been copied from 
            # https://stackoverflow.com/questions/16592915/in-python-how-can-i-get-the-intersection-of-two-lists-preserving-the-order-of
            def sublists(list1, list2):
                subs = []
                for i in range(len(list1)-1):
                    for j in range(len(list2)-1):
                        if list1[i]==list2[j] and list1[i+1]==list2[j+1]:
                            m = i+2
                            n = j+2
                            while m<len(list1) and n<len(list2) and list1[m]==list2[n]:
                                m += 1
                                n += 1
                            subs.append(list1[i:m])
                return subs

            def max_sublists(list1, list2):
                subls = sublists(list1, list2)
                if len(subls)==0:
                    return []
                else:
                    max_len = max(len(subl) for subl in subls)
                    return [subl for subl in subls if len(subl)==max_len]
            
            longest_contiguous = max_sublists(tokenizedQuery,tokenizedSentence)
        
            if longest_contiguous:
                k = len(longest_contiguous[0])
            else:
                k = 0

            l = 0
            if count <=1:
                if count == 0:
                    l = 2
                elif count == 1:
                    l = 1

            score  = c+d+k+h+l
            
            finalTuple = (score*(-1), sentence)
            heap.append(finalTuple)

            count +=1

    # Idea about heap implementation from https://www.geeksforgeeks.org/heap-and-priority-queue-using-heapq-module-in-python/
    # Max heap implementation from https://stackoverflow.com/questions/2501457/what-do-i-use-for-a-max-heap-implementation-in-python
    heapify(heap)
    if len(heap) >=2:
        snippet = heappop(heap)[1] + " "
        snippet = snippet+heappop(heap)[1]
    else:
        if len(heap) == 1:
            snippet = heappop(heap)[1]
        else:
            snippet = "Unable to generate a summary" 

    if metadataDict['headline'] == "":
        metadataDict['headline'] = snippet[:50]+"..."

    line1 = str(rank)+". "+metadataDict['headline']+" ("+metadataDict['date']+")"
    line2 = snippet+" ("+metadataDict['docno']+")"
   
    return line1, line2

# Test Cases
# snippetGen('latimes-index', 1, 'LA010189-0007', 'something')
# snippetGen('latimes-index', 1, 'LA050390-0110', 'something')
# snippetGen('latimes-index', 1, 'LA092590-0006', 'something')