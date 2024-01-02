# This program takes a gzip XML file and directory name as its input
# The program processes gzip file to convert every docs as a seperate file for future retrieval
# Program also creates a document map to retrieve the doc and its relevant metadata
# The program creates inverted index and a lexicon for all the
# contigous alphanumeric term found in these docs
# This program also creates a docLength and Normalized Doc Length File

import sys
import os
import gzip
import Modules.MetaDataExtractor as MetaDataExtractor
import time
import Modules.Tokenizer as Tokenizer

# Record start time
# Code from https://www.educative.io/answers/how-to-measure-elapsed-time-in-python
start_time = time.time()

inputLength = len(sys.argv)

# Get the current directory path
current_directory = os.getcwd()

# Checking if the argument conditions are satisfied
if inputLength == 3:
    fileSource = sys.argv[1]
    docStorage = sys.argv[2]
else:
    if inputLength < 3:
        print("Too few Arguments!")
    else:
        print("Too many arguments!")

    print("This program converts compressed latimes.gz file into separate docs and creates its inverted index.")
    print("Correct input should be latimes.gz and the directory name to store the output.")
    
    sys.exit()

if docStorage.__contains__("/"):
    if not os.path.exists(docStorage):
        os.mkdir(docStorage)
        os.mkdir(docStorage+"/metadata")
        os.mkdir(docStorage+"/docs")
    else:
        print(
            f"A folder with this name already exists in this path'{docStorage}'.")
        sys.exit()
else:
    if not os.path.exists(docStorage):
        os.mkdir(docStorage)
        os.mkdir(docStorage+"/metadata")
        os.mkdir(docStorage+"/docs")
    else:
        print(
            f"A folder with the name '{docStorage}' already exists in '{current_directory}'.")
        sys.exit()

newPath = docStorage+"/"

# Code from
# https://stackoverflow.com/questions/10566558/read-lines-from-compressed-text-files

try:
    with gzip.open(fileSource, 'rt') as f:

        internal_id = 0  # Initialize a document counter
        docIDList = {}  # Initialize a dict for docNo

        # Path and name for the metadata
        metadataFolder = newPath+"metadata/"
        metaDataMap = metadataFolder+'documentMap.txt'
        docLengthLocation = metadataFolder+'doc-Length.txt'
        invertedIndexLocation = metadataFolder+'invIndex.gz'
        lexiconLocation = metadataFolder+'lexicon.txt'
        docLengthNormLocation = metadataFolder+'doc-Length-Norm.txt'

        # Temporary internal variables
        doc = []  # Temporarily stores all the lines of the doc
        headlineArr = []  # Temporarily stores all the lines in Headlines
        headline = ""  # Stores converted Headline
        insideHeadLine = False  # Keeps track of whether pointer is still within Headline tag

        # Inverted Index
        docLength = []
        insideTextLine = False
        insideGraphicLine = False
        tokens = []
        lexicon = {}
        invIndex = []
        docLengthNorm = []

        print("Program is running...")

        # Going through every line in the gz file
        for line in f:
            line = line.strip()
            doc.append(line)

            # Extracting Headline from the texts
            if line == "<HEADLINE>":
                headlineArr.append(line)
                insideHeadLine = True
            elif line == "</HEADLINE>":
                headlineArr.append(line)
                insideHeadLine = False
                headline = MetaDataExtractor.getHeadline(headlineArr)
                headlineArr = []
            elif insideHeadLine:
                headlineArr.append(line)
                tokens.extend(Tokenizer.Tokenize(line))

            if line == "<TEXT>":
                insideTextLine = True
            elif line == "</TEXT>":
                insideTextLine = False
            elif insideTextLine:
                tokens.extend(Tokenizer.Tokenize(line))

            if line == "<GRAPHIC>":
                insideGraphicLine = True
            elif line == "</GRAPHIC>":
                insideGraphicLine = False
            elif insideGraphicLine:
                tokens.extend(Tokenizer.Tokenize(line))

            # Codes to run at the end of the document
            # creates create docNo-id map, stores metadata and stores the txt file for the doc
            if line == "</DOC>":

                docNO = MetaDataExtractor.getDocNo(doc[1])
                docIDList[internal_id] = docNO
                date = MetaDataExtractor.parseDate(docNO)
                docDate = MetaDataExtractor.getDate(date)

                # Assigning Folder Path for the extracted file
                yearFolder = newPath+'docs/'+date['year']
                monthFolder = yearFolder+'/'+date['month']
                dayFolder = monthFolder+'/'+date['day']

                # Logic for creating a new file name
                if not os.path.exists(yearFolder):
                    os.mkdir(yearFolder)
                    os.mkdir(monthFolder)
                    os.mkdir(dayFolder)
                else:
                    if not os.path.exists(monthFolder):
                        os.mkdir(monthFolder)
                        os.mkdir(dayFolder)
                    else:
                        if not os.path.exists(dayFolder):
                            os.mkdir(dayFolder)

                # Path in which this file should be stored
                docPath = dayFolder+'/'+f'{docNO}.gz'
                metadataPath = dayFolder+'/'+f'{docNO}-metadata.txt'

                # Metadata for this file
                # Code produced with ChatGPT
                tempMetaData = [f'docno: {docNO}',
                                f'internal id: {internal_id}',
                                f'date: {docDate}',
                                f'headline: {headline}']

                # writing the data into the disk
                # The following code was produced using ChatGPT
                # The command was to write texts into a gzip file
                with gzip.open(docPath, 'wb') as file_name:
                    for docLines in doc:
                        string_bytes = docLines.encode('utf-8')
                        file_name.write(string_bytes+b'\n')

                # Saves the metadata on the same path
                with open(metadataPath, "w") as file:
                    for lines in tempMetaData:
                        file.write(lines + "\n")

                # Building the Inverted Index
                docLength.append(len(tokens))
                tokenIDs = Tokenizer.ConvertTokensToIDs(
                    tokens, lexicon, invIndex)
                wordCounts = Tokenizer.CountWords(tokenIDs)
                Tokenizer.AddToPostings(wordCounts, internal_id, invIndex)
                docLengthNorm.append(Tokenizer.DocLengthNormalization(wordCounts))

                # Resetting the temporary doc array and incrementing internal id
                doc = []
                internal_id += 1
                tokens = []
                headline = ""

            # ONLY WHILE TESTING: CONDITION TO STOP THE LOOP AT CERTAIN DOC NUMBERS
            # if internal_id == 10:
            #     break

        with open(metaDataMap, "w") as file:
            for key in docIDList:
                file.write(docIDList[key] + "\n")

        with open(docLengthLocation, "w") as file:
            for x in docLength:
                file.write(str(x) + "\n")

        with open(docLengthNormLocation, "w") as file:
            for x in docLengthNorm:
                file.write(str(x) + "\n")

        # The following code has been generated using ChatGPT
        # the code tries to convert the inverted index of array of arrays into text file
        with gzip.open(invertedIndexLocation, 'wb') as file:
            # Write each sub-array as a line
            for sub_array in invIndex:
                # Convert the sub-array to a space-separated string
                line = " ".join(map(str, sub_array))
                line_bytes = line.encode('utf-8')
                file.write(line_bytes + b'\n')

        with open(lexiconLocation, "w") as file:
            for key in lexicon:
                file.write(key + "\n")

    # Record end time
    end_time = time.time()
    elapsed_Time = round(end_time - start_time, 2)
    print(f"Complete! Done within {elapsed_Time} seconds!")

except FileNotFoundError:
    print("Input file does not exist! Please check your input source again!")
    sys.exit()
