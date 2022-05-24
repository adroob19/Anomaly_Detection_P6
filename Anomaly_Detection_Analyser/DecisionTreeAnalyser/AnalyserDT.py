import os.path
import pickle

import numpy as np
from sklearn import tree


class AnalyserDT:

    def __init__(self):
        path = open(os.path.abspath("DecisionTreeAnalyser\\binaryTree.txt"), "rb")
        self.decisionTree = pickle.load(path)
        path.close()

    def predict(self, reading):
        npReading = np.array([reading[2:len(reading)]])
        prediction = self.decisionTree.predict(npReading)
        reading.append(prediction[0])
        return reading
    
