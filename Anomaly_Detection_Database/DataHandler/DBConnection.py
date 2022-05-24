import pyodbc as pyo


class DBConnection():
    def __init__(self):

        self.connection = pyo.connect('Driver={ODBC Driver 18 for SQL Server};'
                                      'Server=(localdb)\MSSQLLocalDB;'
                                      'Database=SensorReadings;'
                                      'Trusted_Connection=yes;')

        self.cursor = self.connection.cursor()

    def storeReading(self, values):
        query = '''
                INSERT INTO dbo.probeReading (probeId, timestamp, luminosity, temperature, humidity, pm10, pm25, no2, co, isAnomaly)
                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Reading stored")
        except Exception as e:
            print(e)

    def storeProbeInformation(self, values):
        query = '''
                INSERT INTO dbo.probe(probeId, location, latitude, longitude)
                VALUES
                (?, ?, ?, ?)
                '''
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            print(e)
        self.connection.commit()

    def retrieveProbeAnomalies(self, serialNumber):
        result = []
        readings = []
        query = """
                SELECT *
                FROM [SensorReadings].[dbo].[probe]
                WHERE [probeId] = ?
                """
        try:
            self.cursor.execute(query, serialNumber)
            for row in self.cursor:
                result.append(row.probeId)
                result.append(row.location)
                result.append(row.latitude)
                result.append(row.longitude)
            print("Anomalies retrieved for probe " + serialNumber)
        except Exception as e:
            print(e)

        query = """
                SELECT TOP(50) *
                FROM [SensorReadings].[dbo].[probeReading]
                WHERE [probeId] = ? AND [isAnomaly] = 1
                ORDER BY CONVERT(DATETIME,[timestamp]) DESC 
                """
        self.cursor.execute(query, serialNumber)
        for row in self.cursor:
            readings.append(
                [row.timestamp, row.luminosity, row.temperature, row.humidity, row.pm10, row.pm25, row.no2, row.co])
        result.append(readings)
        return result

    def retrieveProbeInformation(self):
        result = []
        query = """
                SELECT P.[probeId], [location], [latestAnomaly], [numberOfAnomalies]
                FROM [SensorReadings].[dbo].[probe] as P JOIN (SELECT[probeId], MAX(CONVERT(DATETIME,[timestamp])) as latestAnomaly, COUNT(*) as numberOfAnomalies
                FROM [SensorReadings].[dbo].[probeReading]
                WHERE [isAnomaly] = 1
                GROUP BY probeId) as R ON P.probeId = R.probeId
                ORDER BY latestAnomaly DESC
                """
        try:
            self.cursor.execute(query);
            print("Probe information retrieved")
        except Exception as e:
            print(e)
        for row in self.cursor:
            result.append(
                [row.probeId, row.location, row.latestAnomaly.strftime("%m/%d/%Y %H:%M:%S"), row.numberOfAnomalies])
        return result
