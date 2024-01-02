# This program helps to extract topic ids and queries for each ids from the
# given XML file called 'topics.401-450-xml.txt'

import os
import xml.etree.ElementTree as ET

current_directory = os.getcwd()

QueryFile = current_directory+'/topics.401-450-xml.txt'
outputFile = current_directory+'/queries.txt'

insideTopic = False


with open(QueryFile, "r") as mfile:
    content = mfile.read()

root = ET.fromstring(content)

topicIdList = []
titlesList = []

excludeList = ['416', '423', '437', '444', '447']

# Code from https://stackoverflow.com/questions/7691514/extracting-text-from-xml-using-python
for topic in list(root):
    topicId = topic.find('number').text.strip()
    title = topic.find('title').text.strip()

    # Removes the topics that we don't need
    if topicId not in excludeList:
        topicIdList.append(topicId)
        titlesList.append(title)

# Create a new text file to store the results
# Following code has been generated using ChatGPT
with open(outputFile, 'w') as output_file:

    # Write numbers and titles to the output file
    for num, title in zip(topicIdList, titlesList):
        output_file.write(f"{num}\n{title}\n")

print('Done!')
