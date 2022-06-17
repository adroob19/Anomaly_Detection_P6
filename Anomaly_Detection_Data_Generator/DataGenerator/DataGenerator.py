import random
import time

from DataHandler.DataHandler import DataHandler

class DataGenerator:

    @staticmethod
    def generateReading():
        readings = DataHandler.RetrieveSensorReadings()
        indexForReading = DataHandler.GetRandomIndex()
        anomaly = DataHandler.ProbabilityForAnomaly(1)
        sleepTime = 3
        time.sleep(sleepTime)
        if anomaly == True:
            print("Generating abnormal reading...")
            readingWithAnomaly = DataHandler.generateAnomaly(readings, indexForReading)
            return readingWithAnomaly
        else:
            print("Generating normal reading...")
            return readings.dataInRows[indexForReading]
