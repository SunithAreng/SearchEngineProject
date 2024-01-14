# Sunith Areng - MSCI 541 - Search Engine

You can follow the instructions below to build and run the program.

## Initial Setup Instructions 

1. **Python 3 Installation:**
   - Make sure Python 3 is installed on your computer. If not, you can download it from [here](https://www.python.org/downloads/).
   - Some of the programs may need the pandas package to be installed if it hasn't been installed before.
   - To install pandas on your existing python, run the following command on Command Prompt (on Windows) or Terminal (on Mac):
      ```bash
      pip3 install pandas
      ```

2. **Cloning the Repository:**
   - Use the following link to clone the repository using the `git clone` command:
     ```bash
     git clone https://github.com/SunithAreng/SearchEngineProject.git
     ```
   - Navigate to the directory where the repository was cloned. This directory contains the following  main programs: `SearchEngine`, `IndexEngine`, `GetDoc`, `BM25`, `CosineRank`, `BooleanAND`, and `ResultsEvaluator`.

3. **Sample Data**
   - The codes in this repository were based on TREC Latimes data. However, due to copyright issues such data couldn't be provided in this repo. In its place, a filler script is used following the same data organization structure allowing the code to be run and tested for its merits. This may require the installation of the Faker library in case you want to run your own script to [create the files](#optionalhelper-programs) or simply use the "qatimes.gz" data that is provided on this repo. Simply use the "qatimes.gz" file as a data file to test out the Search Engine UI.

## Interactive Retrieval Interface:
1. **Running SearchEngine Program**
   - To perform BM25 Retrieval using an interactive interface, open your terminal (on Mac) or Command Prompt (on Windows) and run the following command:
     ```bash
     python3 SearchEngine.py STORAGE_PATH/FOLDER_NAME
     ```
   - The program takes in the path of the folder where the data is stored as an argument.
   - The program will load the inverted index and relevant data structures into RAM and prompt the user for their query. The user is allowed to type anything as a query up to pressing the Enter key, which submits the query to the engine.
   - After displaying the results, to view the document of their choice, the user is prompted by the engine to type in the integer rank of the document.
      - The user is shown appropriate instructions in case of invalid inputs.    
      - Having displayed the document, the program will prompt the user again for a rank to view another document until the user decides to try a new query or exit the program.
   - At any given point, the user has the following commands at their disposal:
      - "N" or "n" if they want to enter another query.
      - "Q" or "q" if they want to exit the program.

## Building and Running the Search Engine Programs

1. **Running the IndexEngine Program:**
   - ADDITIONAL STEP: If you wish to stem the words in the documents into stemmed tokens then complete the following steps, otherwise move on to the next step:
      - Open the folder named 'Modules' found on the root directory. This directory holds all the custom-written modules used by the programs in this repository.
      - Open the program, `Tokenizer.py` on a notepad or the IDE of your choice that can read Python code. Visual Studio Code is recommended.
      - Scroll down to the line number 31. This line represents the code that allows the 'IndexEngine' and other retrieval programs (BooleanAND, BM25, CosineRank) to tokenize their terms. There are also comments showing its location in the code.
      - "Uncomment" the line number 31. This will enable PorterStemming for 'IndexEngine' and all the other programs as this module is common for all.
      - To disable PorterStemming, simply follow the above steps and "comment" line number 31. 
   - To extract and process data from the compressed file 'latimes.gz' file, open your terminal (on Mac) or Command Prompt (on Windows) and run the following command:
     ```bash
     python3 IndexEngine.py DATA_PATH/DATAFILE.gz STORAGE_PATH/FOLDER_NAME
     ```
     - Wait for the program to complete. Processing the compressed file and storing documents separately may take some time depending on whether stemming is enabled. While simultaneously creating a lexicon, an inverted index, and documents tracking Document Length and Document Normalized Length.
     - You will receive a completion message on the terminal and the program's runtime duration.
     - Verify that the metadata and the text files have been successfully created and stored on your disk.

2. **Retrieve and Read a Document:**
   - To retrieve a document based on its identifier, run the following command:
     ```bash
     python3 GetDoc.py STORAGE_PATH/FOLDER_NAME idtype id
     ```
     - Replace `idtype` with either of the two input types "docno" or "id".
     - Replace `id` with the actual document number (docno) or the integer identifier specified earlier in the argument.
     - After running the command, the terminal will display metadata followed by the raw document in XML format.

## Information Retrieval Algorithms

### BM25 Retrieval Algorithm

1. **BM25 Retrieval for a list of queries:**
   - To retrieve a list of documents for a given set of queries, run the following command:
     ```bash
     python3 BM25.py STORAGE_PATH/FOLDER_NAME QUERY_FILE.txt OUTPUTFILE_NAME.txt
     ```
   - Replace `QUERY_FILE` with an appropriate name for the file where the list of queries has been stored.
      - `QUERY_FILE.txt` should follow the format of the topic number on one line followed by the actual query on the next line.
      - The repository contains one query-related file in the root directory called "queries.txt" for the instructor-provided topics/queries. This file should be used for this program.
   - Replace `OUTPUTFILE_NAME.txt` with the appropriate output file name.

### Cosine Similarity Retrieval Algorithm

1. **Cosine Similarity Retrieval for a list of queries:**
   - To retrieve a list of documents for a given set of queries, run the following command:
     ```bash
     python3 CosineRank.py STORAGE_PATH/FOLDER_NAME QUERY_FILE.txt OUTPUTFILE_NAME.txt
     ```
   - Replace `QUERY_FILE` with an appropriate name for the file where the list of queries has been stored.
      - `QUERY_FILE.txt` should follow the format of the topic number on one line followed by the actual query on the next line.
      - The repository contains one query-related file in the root directory called "queries.txt" for the instructor-provided topics/queries. This file should be used for this program.
   - Replace `OUTPUTFILE_NAME.txt` with the appropriate output file name.

### BooleanAND Retrieval Algorithm

1. **BooleanAND Retrieval for a list of queries:**
   - To retrieve a list of documents for a given set of queries, run the following command:
     ```bash
     python3 BooleanAND.py STORAGE_PATH/FOLDER_NAME QUERY_FILE.txt OUTPUTFILE_NAME.txt
     ```
   - Replace `QUERY_FILE` with an appropriate name for the file where the list of queries has been stored.
      - `QUERY_FILE.txt` should follow the format of the topic number on one line followed by the actual query on the next line.
      - The repository contains one query-related file in the root directory called "queries.txt" for the instructor-provided topics/queries. This file should be used for this program.
   - Replace `OUTPUTFILE_NAME.txt` with the appropriate output file name.

2. **Running test program for the BooleanAND program:**
   - Navigate to the 'Boolean-test-files' folder where the test program is located.
   ```bash
      cd Boolean-test-files
   ```
   - Ensure the test_Results.txt (output file from BooleanAND sampleDocs test_Query) is in the same directory as the test program.
   - To run the automated test, run the following command:
      ```bash
      python3 testBooleanAND.py
      ```
   - The output on the terminal should show 'OK', which means all the test cases have passed.

### Creating a query file for retrieval

1. **Extracting queries from the topics document**
   - The "queries.txt" for the instructor-provided queries can be created by running the `QueryExtractor` program for the topics 401-450 XML text file. 
   - Ensure the "topics.401-450-xml.txt" file is in the same root directory as the program.
   - Run the following command:
     ```bash
     python3 QueryExtractor.py
     ```
   - The output will generate a "queries.txt" file in the same directory in the required format (topic id and query) to be used by the retrieval programs.

## Evaluation of Search Engine Results

1. **Running ResultsEvaluator Program to evaluate IR results**
   - To evaluate a TREC results file, run the following command on terminal (on Mac) or Command Prompt (on Windows):
      ```bash
      python3 ResultsEvaluator.py QREL_FILE_PATH/QREL_FILENAME RESULTS_FILE_PATH/RESULTS_FILE_NAME  
      ```
   - Replace `QREL_FILE_PATH` with the path to the folder where the qrels file is stored.
      - In case the qrel file is in the root directory, then this step is not needed.
   - Replace `QREL_FILENAME` with an appropriate name for the qrel file. Make sure to include ".txt" in case the file is in a text format.
   - Replace `RESULTS_FILE_PATH` with the path to the folder where the results file has been stored.
      - In case the results file is in the root directory, then this step is not needed.
   - Replace `RESULTS_FILE_NAME` with the name of the results file. Make sure to include ".txt" in case the file is in a text format.
   - The output for this program can be found in a folder called "Evaluated_Results" in the root directory, which is created when the program is run. 
      - The output file will be named after the run id found in the results file followed by "-measures.txt". Example, "student1-measures.txt"
   - The program outputs an error message in the terminal in case of bad format for the results files.

Some helpful programs to automate results evaluation and collect statistics. [Click Here](#optionalhelper-programs)

## Optional/Helper Programs

1. **Measures Automation**
   - This program runs the ResultsEvaluator program in the loop while going over all the results files.
   - The program exists in the root directory and assumes there is a folder called "results-files" with all the results files.
   - To run this program, run the following command on the terminal:
      ```bash
      python3 MeasuresAutomation.py 
      ```
   - The program will then look at the folder for all filenames having the 'results' term in them and execute the ResultsEvaluator Program. It will display an error message accordingly.

2. **Calculating Results Statistics**
   - This program calculates the averages for all the existing measures for each of the evaluated results files and consolidates them all in one file.
   - The program assumes there is a folder called "Evaluated_Results" in the root directory which it uses to calculate statistics.
   - To run this program, run the following command on the terminal:
      ```bash
      python3 ResultsStats.py
      ```
   - The output is a text file "stats.txt" which is created in the root directory as the program.
  
3. **Running the Filler Script**
   - First, install Faker Library. For this run the following command on your terminal.
     ```bash
      pip3 install faker
      ```
   - Then make sure to navigate to the directory where this repo is stored and simply run the following code on the terminal:
      ```bash
      python3 fillerscript.py
      ```
   - Upon running the code it should generate "qatimes" document on the same directory. This file needs to be converted to a gzip file. To convert into a gzip file on Mac with its built-in feature, run the following code on Terminal:
      ```bash
      gzip qatimes
      ```
   - This should now create a qatimes.gz data file in the main directory. Simply use this file from here on now and follow the remaining instructions.
