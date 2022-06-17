import os
import csv
import random
import sys
from urllib.request import DataHandler

import numpy as np

from DataHandler.Readings import Readings


class DataHandler:

    @staticmethod
    def RetrieveSensorReadings():
        listOfSensorReadings = []
        file = open('DataHandler/CityProbeData.csv')
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            for num in range(20, len(row) - 1):
                if row[num] == '':
                    row[num] = float("nan")
                row[num] = float(row[num])
            if all(float(i) < 15000 for i in row[20: len(row) - 1]):
                listOfSensorReadings.append(row[20:len(row) - 1])
        file.close()
        return Readings(listOfSensorReadings, header[20:len(header) - 1])

    @staticmethod
    def GetRandomIndex():
       randomNumber = random.choice(range(0, 1599))
       return randomNumber

    @staticmethod
    def ProbabilityForAnomaly(probability):
        return random.random() < probability

    @staticmethod
    def generateAnomaly(readings, randomNumber): #number of colums we want anomalies in
        i = 0
        columns = []
        valueForHighDeviation = random.randint(0,1)
        valueforDirection = random.randint(0,1)
        numberOfFeaturesWithAnomalies = random.randint(0,6)

        while i < numberOfFeaturesWithAnomalies:
            num = random.randint(0, len(readings.headers) - 1)
            if not columns.__contains__(num):
                columns.append(num)
                i = i + 1

        for item in columns:
            std = readings.stdDeviations[item]
            maxVal = max(readings.yVals[item]) + std
            minVal = min(readings.yVals[item]) - std

            if valueForHighDeviation == 1:
                deviation = "high"
            else:
                deviation = "low"

            if valueforDirection == 1:
                direction = "up"
            else:
                direction = "down"

            if deviation == "high":
                if direction == "up":
                    value = random.uniform(maxVal + std, maxVal + 2 * std)
                else:
                    value = random.uniform(minVal - std, minVal - 2 * std)
            else:
                if direction == "up":
                    value = random.uniform(maxVal + 0.01, maxVal + std)
                else:
                    value = random.uniform(minVal - 0.01, minVal - std)

            readings.dataInRows[randomNumber][item] = round(value, 2)
        return readings.dataInRows[randomNumber]

    @staticmethod
    def GetProbeInformation():
        file = open('DataHandler/CityProbeData.csv')
        csvreader = csv.reader(file)
        header = next(csvreader)
        row = next(csvreader)
        probeid = row[header.index("serial")]
        location = row[header.index("desc")]
        lat = row[header.index("lat")]
        lon = row[header.index("lon")]
        return [probeid, location, lat, lon]