import json
import logging
import time

from signalrcore.hub_connection_builder import HubConnectionBuilder
from sklearn import tree

from DecisionTreeAnalyser.AnalyserDT import AnalyserDT


class Interface:
    hub_connection = None
    end = False
    dictionaryOfConnections = {}
    _sourceDecisionTree = tree.DecisionTreeClassifier()

    def __init__(self):
        self.connectToHub()

    def connectToHub(self):
        self.hub_connection = HubConnectionBuilder() \
            .with_url("http://localhost:8081/Hub") \
            .with_automatic_reconnect({
            "type": "raw",
            "keep_alive_interval": 10,
            "reconnect_interval": 5,
        }) \
            .configure_logging(logging.INFO) \
            .build()
        self.hub_connection.on_open(lambda: self.onConnection())
        self.hub_connection.on_close(lambda: print("connection closed"))
        self.hub_connection.on("addProbe", self.addProbe)
        self.hub_connection.on("removeProbe", self.removeProbe)
        self.hub_connection.on("AnalyseReading", self.AnalyseReading)
        self.hub_connection.start()

        while not self.end:
            time.sleep(1)

        self.hub_connection.stop()

    def onConnection(self):
        print("connection opened and handshake received")
        self.hub_connection.send("AnalyserConnect", [])

    def addProbe(self, message):  # message = [serialNumber]
        print("probe connected")
        self.dictionaryOfConnections[message[0]] = AnalyserDT()

    def removeProbe(self, message):  # message = [serialNumber]
        print("probe disconnected")
        if message[0] in self.dictionaryOfConnections:
            del self.dictionaryOfConnections[message[0]]

    def AnalyseReading(self, message):  # message = [probeConnectionID, reading]
        print("Reading received, analysing...")
        reading = json.loads(message[1])
        if not message[0] in self.dictionaryOfConnections:
            self.dictionaryOfConnections[message[0]] = AnalyserDT()
        try:
            reading = self.dictionaryOfConnections[message[0]].predict(reading)
            reading[len(reading) - 1] = int(reading[len(reading) - 1])
            readingJsonDumps = json.dumps(reading)
            self.hub_connection.send("SendMessage", [message[0], "Analyser:NewPrediction", readingJsonDumps])
            print("Labelled reading returned to hub")
        except Exception as e:
            print(e)
