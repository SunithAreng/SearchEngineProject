# This program contains several useful functions that are used to
# create inverted index and lexicon by the IndexEngine.py

import re
import math
# from nltk.stem import PorterStemmer
from Modules.PorterStemmer import PorterStemmer

# Converts a string (single line) into tokens
# Returns an array with all words as a single token
def Tokenize(docLine):
    removeList = ['<HEADLINE>', '</HEADLINE>', '<P>', '</P>', '<TEXT>',
                  '</TEXT>', '<GRAPHIC>', '</GRAPHIC>']

    tokens = []

    if docLine not in removeList:
        docLine = docLine.lower()
        p = PorterStemmer()

        # The code was generated using ChatGPT
        # Split the string based on punctuations
        words = re.findall(r'\w+', docLine)

        for token in words:
            if len(token) > 1 and not token.isdigit():

                # ----- Uncomment the line below for stemming -----------

                # token = p.stem(token,0,len(token)-1) #Porter Website version

                # ----- Uncomment upto the above line for stemming ----------
                
                # token = p.stem(token) #NLTK version -- extra

                tokens.append(token)

    return tokens


# Converts all the tokens found in one doc to token ids
# In case new word/token is encountered, it is added to the lexicon
# lexicon {token: id}
# Returns a list with all the words/tokens converted into their ids
def ConvertTokensToIDs(tokens, lexicon, invIndex):
    tokenIDs = []

    for token in tokens:
        if token in lexicon:
            tokenIDs.append(lexicon[token])
        else:
            id = len(lexicon)
            lexicon[token] = id
            tokenIDs.append(id)
            arr = []
            invIndex.insert(id, arr)

    return tokenIDs


# Returns a dict with term id and its count within the same doc
# dict is {id1: count, id2: count}
def CountWords(tokenIDs):
    wordCount = {}

    for id in tokenIDs:
        if id in wordCount:
            wordCount[id] = wordCount[id]+1
        else:
            wordCount[id] = 1

    return wordCount


# Add the word and count to the bigger inverted Index
# Happens for one doc at a time
def AddToPostings(wordCounts, docID, invIndex):
    for termID in wordCounts:
        count = wordCounts[termID]
        postings = invIndex[termID]
        postings.append(docID)
        postings.append(count)

# The following function normalizes the document length
def DocLengthNormalization(wordCounts):
    normLen = 0
    for termID in wordCounts:
        count = wordCounts[termID]
        normLen += (1+math.log(count))**2

    final = math.sqrt(normLen)
    return final
