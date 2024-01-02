# This program retrieves the metadata and the raw XML document for the given input
# Input: Directory storing documents, id type (docno or id) and the id (latimes docno or integer id)

import sys
import os
import Modules.MetaDataExtractor as MetaDataExtractor
import gzip

inputLength = len(sys.argv)

# Get the current directory path
current_directory = os.getcwd()

# Checking if the argument conditions are satisfied
if inputLength == 4:
    fileSource = sys.argv[1]
    idType = sys.argv[2]
    idInput = sys.argv[3]
else:
    if inputLength < 4:
        print("Too few Arguments!")
    else:
        print("Too many arguments!")
    sys.exit()

if not os.path.exists(fileSource):
    print("This file path does not exist. Please revise your input!")
    sys.exit()

# File source for the metadata assuming IndexEngine has been run
metadataMapFileSource = fileSource+"/metadata/documentMap.txt"

internal_id = 0
id_to_doc_map = {}
doc_to_id_map = {}

with open(metadataMapFileSource, "r") as file:
    for z in file:
        z = z.strip()
        id_to_doc_map[internal_id] = z
        doc_to_id_map[z] = internal_id
        internal_id += 1

result = "404 Not Found"


# Checks for the idtype of the argument input by the user
if idType == 'id':

    # Handing errors https://realpython.com/python-keyerror/

    try:
        # obtains docno from document mapping and performs validation check
        try:
            int(idInput)
        except:
            print("Please provide an integer!")
            sys.exit()

        docNumber = id_to_doc_map[int(idInput)]

    except KeyError:
        print("This id does not exist! Please revise your input!")
        sys.exit()

    date = MetaDataExtractor.parseDate(docNumber)

elif idType == 'docno':

    # Handing errors https://realpython.com/python-keyerror/
    try:
        # checks if the docno exists
        result = doc_to_id_map[idInput]
    except KeyError:
        print("This DOCNO does not exist! Please revise your input!")
        sys.exit()
    date = MetaDataExtractor.parseDate(idInput)
    docNumber = idInput
else:
    print("Invalid id type. Accepted input is either 'id' or 'docno'!")
    sys.exit()

# Extracts date from the docno to obtain path for the doc file

file = fileSource+"/docs/"+date['year']+"/" + \
    date['month']+"/"+date['day']+"/"+docNumber+".gz"
metaDataFile = fileSource+"/docs/" + \
    date['year']+"/"+date['month']+"/" + \
    date['day']+"/"+docNumber+"-metadata.txt"

with open(metaDataFile, "r") as mfile:
    for mtLine in mfile:
        mtLine = mtLine.strip()
        print(mtLine)

# Code from
# https://stackoverflow.com/questions/10566558/read-lines-from-compressed-text-files
print("raw document: ")
with gzip.open(file, 'rt') as f:
    for line in f:
        line = line.strip()
        print(line)
