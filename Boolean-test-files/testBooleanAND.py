# This is a test program to verify the correct output for the test queries for
# the sample docs. The passing of this test program signifies that BooleanAND program
# runs correctly and retrieves all the relevant documents as per its conditions.

import pandas as pd
import unittest
# incase pandas has not been installed then run the following
# command 'pip3 install pandas'


def createDataFrame():
    testResults = "test_Results.txt"
    outputHeader = ['topicID', 'Q0', 'docno', 'rank', 'score', 'runTag']
    df = pd.read_csv(testResults, sep=' ', names=outputHeader)

    return df


# Unit testing from https://docs.python.org/3/library/unittest.html
# 11 test cases were created to test 11 queries.
class TestResultsBySampleQuery(unittest.TestCase):

    def test_query101(self):
        df = createDataFrame()
        queryID = 101

        expected_output = 'QA040499-0001'

        result = df[df['topicID'] == queryID]['docno'].values

        self.assertIn(expected_output, result)

    def test_query102(self):
        df = createDataFrame()
        queryID = 102

        expected_output = ['QA040499-0001', 'QA101699-0001']
        not_expected = ['QA110399-0001', 'QA120399-0002']

        result = df[df['topicID'] == queryID]['docno'].values

        self.assertIn(expected_output, result)
        self.assertNotIn(not_expected, result)

    def test_query103(self):
        df = createDataFrame()
        queryID = 103

        expected_output = ['QA040499-0001', 'QA101699-0001', 'QA120399-0002']
        not_expected = ['QA110399-0001']

        result = df[df['topicID'] == queryID]['docno'].to_numpy()

        self.assertIn(expected_output, result)
        self.assertNotIn(not_expected, result)

    def test_query104(self):
        df = createDataFrame()
        queryID = 104

        expected_output = ['QA120399-0002']
        not_expected = ['QA120399-0003']

        result = df[df['topicID'] == queryID]['docno'].values

        self.assertIn(expected_output, result)
        self.assertNotIn(not_expected, result)

    def test_query105(self):
        df = createDataFrame()
        queryID = 105

        with self.assertRaises(KeyError):
            df[queryID]

    def test_query106(self):
        df = createDataFrame()
        queryID = 106

        with self.assertRaises(KeyError):
            df[queryID]

    def test_query107(self):
        df = createDataFrame()
        queryID = 107

        expected_output = ['QA110399-0001']
        not_expected = ['QA120399-0001']

        result = df[df['topicID'] == queryID]['docno'].values

        self.assertIn(expected_output, result)
        self.assertNotIn(not_expected, result)

    def test_query108(self):
        df = createDataFrame()
        queryID = 108

        not_expected = ['QA120399-0003']

        result = df[df['topicID'] == queryID]['docno'].values

        self.assertNotIn(not_expected, result)

    def test_query109(self):
        df = createDataFrame()
        queryID = 109

        with self.assertRaises(KeyError):
            df[queryID]

    def test_query110(self):
        df = createDataFrame()
        queryID = 110

        expected_output = ['QA040499-0001', 'QA101699-0001']
        not_expected = ['QA120399-0002']

        result = df[df['topicID'] == queryID]['docno'].values

        self.assertIn(expected_output, result)
        self.assertNotIn(not_expected, result)

    def test_query111(self):
        df = createDataFrame()
        queryID = 111

        expected_output = 'QA040499-0001'

        result = df[df['topicID'] == queryID]['docno'].values

        self.assertIn(expected_output, result)


if __name__ == '__main__':
    unittest.main()
