# This program represents a results object that stores the student produced results
# This program is a copy of the instructor provided code
# Results is a dictionary that stores all the results
# Key: query_id, value: result object

# Original Author: Nimesh Ghelani based on code by Mark D. Smucker
# With some modifications by Sunith F. Areng

from collections import defaultdict


class Result:
    def __init__(self, doc_id, score, rank):
        self.doc_id = doc_id
        self.score = score
        self.rank = rank


class Results:
    def __init__(self):
        self.query_2_results = defaultdict(list)

    def add_result(self, query_id, result):
        self.query_2_results[query_id].append(result)

    def get_result(self, query_id):
        return self.query_2_results.get(query_id, None)
