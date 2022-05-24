import unittest
from sklearn import tree
from DecisionTreeAnalyser.AnalyserDT import AnalyserDT
class testAnalyserDT(unittest.TestCase):
    def test_AnalyserType(self):
        test = AnalyserDT()
        self.assertEqual(type(test.decisionTree), tree.DecisionTreeClassifier)
