import pandas as pd
import actipy
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from PlotsForSportData import measurementTimeVector
import seaborn as sns


def fftCoordinates(acceleration):
    fftCoord = np.fft.fftn(acceleration)
    plt.plot(np.abs(fftCoord[0:int(len(fftCoord)/2)]))
    plt.show()

