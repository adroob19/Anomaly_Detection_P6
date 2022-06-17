import datetime
import json
import logging
import time

from signalrcore.hub_connection_builder import HubConnectionBuilder
from DataGenerator.DataGenerator import DataGenerator
from DataHandler.DataHandler import DataHandler


class Interface:
    hub_connection = None
    end = False
    connectionId = None

    def __init__(self):
        self.connectToHub()
        self.generate = True

    def connectToHub(self):
        self.hub_connection = HubConnectionBuilder() \
            .with_url("http://localhost:8081/Hub") \
            .with_automatic_reconnect({
            "type": "raw",
            "keep_alive_interval": 10,
            "reconnect_interval": 5,
        }) \
            .build()
        self.hub_connection.on_open(lambda: self.onConnection())
        self.hub_connection.on_close(lambda: print("connection closed"))
        self.hub_connection.start()

        while not self.end:
            time.sleep(1)

        self.hub_connection.stop()

    def onConnection(self):
        print("connection opened and handshake received")
        self.hub_connection.send("addProbe", DataHandler.GetProbeInformation())
        self.generatorStart()

    def generatorStart(self):
        while True:
            reading = DataGenerator.generateReading()
            reading.insert(0, datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            reading.insert(0, DataHandler.GetProbeInformation()[0])
            self.sendReadingToHub(reading)

    def sendReadingToHub(self, reading):
        try:
            readingJsonDumps = json.dumps(reading)
            self.hub_connection.send("SendMessage", ["", "Input:NewReading", readingJsonDumps])
            print("Reading sent to hub")
        except Exception as e:
            print(e)
