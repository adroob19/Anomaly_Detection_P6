import json
import logging
import time
from signalrcore.hub_connection_builder import HubConnectionBuilder
from DataHandler.DBConnection import DBConnection


class Interface:
    hub_connection = None
    end = False
    dbconnection = DBConnection()

    def __init__(self):
        self.connectToHub()

    def connectToHub(self):
        self.hub_connection = HubConnectionBuilder() \
            .with_url("http://localhost:8081/Hub") \
            .with_automatic_reconnect({
            "type": "raw",
            "keep_alive_interval": 10,
            "reconnect_interval": 5,
        }).build()
        self.hub_connection.on_open(lambda: self.onConnection())
        self.hub_connection.on_close(lambda: print("connection closed"))
        self.hub_connection.on("StoreReading", self.storeReading)
        self.hub_connection.on("StoreProbeInformation", self.storeProbeInformation)
        self.hub_connection.on("RetrieveProbeInformation", self.retrieveProbeInformation)
        self.hub_connection.on("RetrieveProbeAnomalies", self.retrieveProbeAnomalies)
        self.hub_connection.start()

        while not self.end:
            time.sleep(1)

        self.hub_connection.stop()

    def onConnection(self):
        print("connection opened and handshake received")
        self.hub_connection.send("DatabaseConnect", [])

    def storeReading(self, message):  # message = [Reading]
        print("Reading received, storing...")
        jsonLoads = json.loads(message[0])
        self.dbconnection.storeReading(jsonLoads)
        try:
            if (jsonLoads[len(jsonLoads) - 1] == 1):  # If IsAnomaly = 1
                self.retrieveProbeInformation(["FrontPageGroup"])
        except Exception as e:
            print(e)

    def storeProbeInformation(self, message):  # message = [serial, location, lat, lon]
        self.dbconnection.storeProbeInformation(message)

    def retrieveProbeInformation(self, message):  # message = [ConnectionID]
        print("Retrieving probe information")
        probeInformation = self.dbconnection.retrieveProbeInformation()
        self.sendProbeInformationToHub(message[0], probeInformation)

    def sendProbeInformationToHub(self, groupName, probeInformation):
        try:
            probeInformationJsonDumps = json.dumps(probeInformation)
            self.hub_connection.send("SendMessage", [groupName, "Database:ProbeInformation", probeInformationJsonDumps])
        except Exception as e:
            print(e)

    def retrieveProbeAnomalies(self, message):  # message = [ConnectionID, SerialNumber]
        print("Retrieving anomalies for probe " + message[1])
        probeAnomalies = self.dbconnection.retrieveProbeAnomalies(message[1])
        self.sendProbeAnomaliesToHub(message[0], probeAnomalies)

    def sendProbeAnomaliesToHub(self, groupName, probeAnomalies):
        try:
            probeAnomaliesJsonDumps = json.dumps(probeAnomalies)
            self.hub_connection.send("SendMessage", [groupName, "Database:ProbeAnomalies", probeAnomaliesJsonDumps])
        except Exception as e:
            print(e)
