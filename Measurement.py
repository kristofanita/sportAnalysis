import numpy as np
import pandas as pd
import datetime
from PlotsForSportData import accelerationDataframe
from hrvanalysis import get_time_domain_features


class Measurement:
    def __init__(self):
        self.rrList = list()
        self.accList = list()
        self.startMeasure = datetime.datetime(1000,1,1,00,00,00, 000)
        self.endMeasure = datetime.datetime(1000,1,1,00,00,00, 000)
        self.processedAcc = pd.DataFrame()

    def __int__(self, rr, acceleration, rr_features):
        self.rrList.append(rr)
        self.accList.append(acceleration)

    def addRRListToMeasurement(self, rrL):
        self.rrList.append(rrL)

    def addACCListToMeasurement(self, accL):
        self.accList.append(accL)

    def accelerationToCSV(self, path):
        df = self.getDFacceleration()
        pd.to_datetime(df ['time'], format="%Y-%m-%d %H:%M:%S:%f")
        df.to_csv(path, sep=',', header=True, index=False)

    def get_rr_features(self):
        return get_time_domain_features(self.rrList)

    def getDFacceleration(self):
        xList = []
        yList = []
        zList = []
        for acc in self.accList:
            xList.append(acc.x)
            yList.append(acc.y)
            zList.append(acc.z)
        timeVector = self.create_acceleration_time_vector(len(xList))
        accDF = pd.DataFrame(timeVector, columns=['time'])
        accDF['x'] = xList
        accDF['y'] = yList
        accDF['z'] = zList
        accDF[['x', 'y', 'z']] = accDF[['x', 'y', 'z']].apply(pd.to_numeric, errors='coerce')
        accDF['time'] = pd.to_datetime(accDF['time'], errors='coerce')
        accDF['time'] = accDF['time'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + accDF['time'].dt.strftime('%z')

        # Handle potential NaN values
        accDF['time'] = accDF['time'].apply(lambda x: str(x)[:-3] if not pd.isna(x) else x)  # + '+0100 [Europe/London]'

        accDF = accDF.dropna()

        # Reset the index after dropping rows
        accDF = accDF.reset_index(drop=True)
        print("EEEEEEEEE")
        print(accDF.head())
        return accDF

    def measurement_start_time(self, startDateTime):
        self.startMeasure = datetime.datetime.strptime(startDateTime, '%d.%m.%Y %H:%M:%S')
        return self.startMeasure

    def create_acceleration_time_vector(self, n):
        t = list()
        for i in range(n):
            sec = 0.08 * i
            t_i = self.startMeasure + datetime.timedelta(seconds=sec)
            t.append(t_i)
        return t

    def getProcessedAcc(self):
        self.processedAcc = pd.read_csv("src/accDataProcessed.csv")
        return self.processedAcc
