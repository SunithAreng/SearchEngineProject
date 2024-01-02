# This program provides a user interface to perform a BM25 Retrieval on Terminal
# It requires one argument - path/folder_name of the index
# User is required to type their query, provide rank number to read the document
# Other commands include n for new query and q for exiting the program
# The program also provides messages to the user about the appropriate commands in case of errors

import sys
from Modules.BM25GUI import BM25_Retrieval, invIndexLoading
from Modules.GetDocGUI import GetDoc
from Modules.snippetGenerator import snippetGen
import time

inputLength = len(sys.argv)

if inputLength == 2:
    fileSource = sys.argv[1]
else:
    if inputLength < 2:
        print("Too few Arguments!")
    else:
        print("Too many arguments!")
    print("This program provides an interface for the user to search and retrieve documents using an inverted index.")
    print("Correct argument will be storage_path/folderName of where the index is stored.")    
    sys.exit()

def UserInput(results, data):
    rank = input("Enter the rank of the document you'd like to see :")
    if rank.isdigit():
        r = int(rank)
        if 1 <= r <= len(results):
            docno = results[r]
            print()
            GetDoc(fileSource, docno)
            print()
        else:
            print()
            print(f'Please input integer values for rank between 1 and {len(results)}')
            print()

        UserInput(results, data)
    elif rank.lower() == 'q':
        sys.exit()
    elif rank.lower() == 'n':
        UserQuery(data)
    else:
        print()
        print("Enter an integer for rank (or 'q' to exit, 'n' for a new query):\n")
        UserInput(results, data)

def UserQuery(data):
    print()
    query = input("Enter your query: ")
    print()
    if query.lower() == "q":
        sys.exit()
    elif query.lower() == 'n':
        UserQuery(data)
    else:
        start_time = time.time()
        results = BM25_Retrieval(query, data)
        
        if results: 
            for x in results:
                docno = results[x]
                snippet = snippetGen(fileSource, x, docno, query)
                print(snippet[0])
                print(snippet[1])
                print()
        else:
            print('Your query retruned no results! Please provide another query.')
            print()
        
        # Print retrieval time
        end_time = time.time()
        elapsed_Time = round(end_time - start_time, 2)
        print(f"Retrieval Complete! Duration: {elapsed_Time} seconds.")

        if results:
            print()
            UserInput(results, data)
        else:
            UserQuery(data)

start_time = time.time()
print("Loading Inverted Index...")

data = invIndexLoading(fileSource)

end_time = time.time()
elapsed_Time = round(end_time - start_time, 2)

print()
print(f"Data Loaded! Duration: {elapsed_Time} seconds.")

UserQuery(data)