# This program contains classes that parses both qrels and results file into
# objects that will be used by our evaluation program

from Modules.qrels import Qrels, Judgement
from Modules.Results import Results, Result

# Author: Nimesh Ghelani based on code by Mark D. Smucker
# Some of the codes have been modified by Sunith F. Areng


class ResultsParseError(Exception):
    pass


class ResultsParser:

    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        global_run_id = None
        history = set()
        results = Results()

        with open(self.filename) as f:
            for line in f:
                line_components = line.strip().split()
                if len(line_components) != 6:
                    raise ResultsParseError(
                        'lines in results file should have exactly 6 columns')

                query_id, _, doc_id, rank, score, run_id = line_components
                rank = int(rank)
                score = float(score)

                if global_run_id is None:
                    global_run_id = run_id
                elif global_run_id != run_id:
                    raise ResultsParseError(
                        'Mismatching runIDs in results file')

                key = query_id + '-' + doc_id
                if key in history:
                    raise ResultsParseError(
                        'Duplicate query_id, doc_id pair in results file')
                history.add(key)

                results.add_result(query_id, Result(doc_id, score, rank))

        # The code below sorts the results dictionary in the descending order of score
        # Code from https://stackoverflow.com/questions/403421/how-do-i-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
        for id in results.query_2_results:
            results.query_2_results[id].sort(
                key=lambda x: (x.score, x.doc_id), reverse=True)

        return global_run_id, results


class QrelsParseError(Exception):
    pass


class QrelsParser:

    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        qrels = Qrels()
        with open(self.filename) as f:
            for line in f:
                line_components = line.strip().split()
                if len(line_components) != 4:
                    raise QrelsParseError("Line should have 4 columns")
                query_id, _, doc_id, relevance = line_components
                relevance = int(relevance)
                qrels.add_judgement(Judgement(query_id, doc_id, relevance))
        return qrels
