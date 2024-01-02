import pandas as pd

topicId = 427

csv_file_path = "qrels/qrels.tsv"

column_names = ['topicID', 'Q0', 'Docno', 'Relevance']

df = pd.read_csv(csv_file_path, sep=' ', names=column_names)

filtered_df = df[(df['topicID'] == topicId) & (df['Relevance'] == 1)]

print(filtered_df)
