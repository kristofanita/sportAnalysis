import actipy
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import pandas as pd
import math
from sklearn.preprocessing import StandardScaler, normalize
from scipy.signal import hilbert
import seaborn as sns
from scipy.signal import butter, sosfiltfilt


def plotDiffRR(rrList):
    X = measurementTimeVector(rrList)
    plt.plot(X, rrList)
    plt.title("R-R peaks time-differences")
    plt.xlabel("sample")
    plt.ylabel("time difference between R-R peaks (ms)")
    plt.show()

    plt.figure(figsize=(12, 8))
    plt.title("Distribution of RR Intervals", fontsize=20)
    plt.xlabel("Time (ms)", fontsize=15)
    plt.ylabel("Number of RR Interval per bin", fontsize=15)
    minRR = math.floor(min(rrList)) - 10
    maxRR = math.floor(max(rrList)) + 10
    bin_length = 8
    plt.hist(rrList, bins=range(minRR, maxRR, bin_length), rwidth=0.8)
    plt.show()

def timeOfMeasurement(rrList):
    summaTime = 0
    for t in rrList:
        summaTime = summaTime + t
    return summaTime

def measurementTimeVector(rrList):
    summaTime = timeOfMeasurement(rrList)
    return np.linspace(0, math.floor(summaTime), len(rrList))

def accelerationDataframe(accList):
    xList = []
    yList = []
    zList = []
    for acc in accList:
        xList.append(acc.x)
        yList.append(acc.y)
        zList.append(acc.z)
    accDF = pd.DataFrame(xList, columns=['x'])
    accDF['y'] = yList
    accDF['z'] = zList
    return accDF


def plotMovements(accList):
    # fig = plt.figure()
    df = accelerationDataframe(accList)
    plt.plot(df.x, 'b')
    plt.plot(df.y, 'g')
    plt.plot(df.z, 'r')
    plt.title("Acceleration")
    plt.show()

def plot_together(rrList, accList):
        T1 = measurementTimeVector(rrList)
        rrDF = pd.DataFrame(rrList, columns=['rr'])
        rrDF['scaledRR'] = rrDF['rr'] / 20
        hossz = int(len(rrDF) / 20)
        hilb = np.abs(hilbert(rrDF['scaledRR'], axis=0))
        winDf = pd.DataFrame(data={"y": hilb}, index=T1)
        windowsize = 500
        winDf['upper_envelop'] = winDf['y'].rolling(window=windowsize).max().shift(int(-windowsize / 2))

        T2 = np.linspace(0, timeOfMeasurement(rrList), len(accList.x))
        print("TTTTTTTTTTTTT222222222222")
        print(T2)

        accList['time'] = pd.to_datetime(accList['time'], utc=False)
        accList.set_index('time', inplace=True)
        hours = pd.date_range(accList.index.min(), accList.index.max(), freq='1H')
        print(hours)

        plt.figure(figsize=(12, 6))
        accList['vectorial_sum'] = (accList['x'] ** 2 + accList['y'] ** 2 + accList['z'] ** 2) ** 0.5
        accList.vectorial_sum = abs(accList.vectorial_sum - np.mean(accList.vectorial_sum))
        #sns.lineplot(data=accList, x=T2, y='vectorial_sum', linewidth=0.8, color='blue')
        plt.plot(T2, accList['vectorial_sum'], 'g')
        #plt.xticks(accList.time, accList.time.strftime('%H:%M:%S'), rotation=45, ha='right')

        plt.plot(T1, winDf['upper_envelop'], 'k')
        plt.title("Acceleration - HRV")
        plt.xlabel("time (ms)")
        plt.legend(["movement", "envelope of HRV"])
        plt.show()

