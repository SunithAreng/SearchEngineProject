# This program contains several useful functions used by the IndexEngine program
# Functionalities include getting metadata, parsing XML documents

import xml.etree.ElementTree as ET
import calendar


# The code below for this function has been obtained from ChatGPT
# The code uses XML parser to remove tags to obtain docno
def getDocNo(line):
    # Parse the XML content
    root = ET.fromstring(line)

    # Extract and print the text content
    docNo = root.text.strip() if root.text else ""

    return docNo


# The function below removes all the tags and only keeps the text content for headlines
def getHeadline(array):
    removeList = ['<HEADLINE>', '</HEADLINE>', '<P>', '</P>']
    headline = ""

    # The code below was generated using ChatGPT
    new_list = [x for x in array if x not in removeList]

    for x in new_list:
        headline = headline+" "+x

    return headline


# The function below creates date in word form converting month
def getDate(dateDict):

    # Idea obtained from https://pynative.com/python-get-month-name-from-number/
    month = calendar.month_name[int(dateDict['month'])]
    day = str(int(dateDict['day']))

    # Sorry not sure how to handle year 2000 problem
    return month + " "+day+", 19"+dateDict['year']


# The function parses docno to extract year, month and day
def parseDate(docNO):
    date = {'month': docNO[2:4],
            'day': docNO[4:6],
            'year': docNO[6:8]}
    return date
