import numpy as np
import pandas as pd

from Coordinates import Coordinates
from Measurement import Measurement
from Person import Person
from PlotsForSportData import plotDiffRR, plotMovements, plot_together, measurementTimeVector, accelerationDataframe
import xml.etree.ElementTree as ET
import re
from HRVAnalysis import preprocessRR, featureRRplots, rrFeatureExtraction
from Acceleration import fftCoordinates
from datetime import datetime, timedelta
import actipy


def setVariablesFromXml(personInfo):
    tree = ET.parse('src/data.xml')
    root = tree.getroot()
    person = Person()
    for personXML in root.iter("PersonBackgroundInfo"):
        for info in personXML:
            match info.tag:
                case "Firstname":
                    person.firstName = info.text
                case "Lastname":
                    person.lastName = info.text
                case "Gender":
                    person.gender = info.text
                case "DateOfBirth":
                    person.dateOfBirth = info.text
                case "Height":
                    person.height = info.text
                case "Weight":
                    person.weight = info.text
                case "ActivityClass":
                    person.activityClass = info.text
                case "MaxHR":
                    person.maxHR = info.text
                case "MinHR":
                    person.minHR = info.text
                case _ :
                    raise Exception("Date provided can't be determined as Person background information: ", info.text)

    for m in root.iter("Measurement"):
        oneMeasurement = Measurement()
        tmpRRList = list()
        for rr in m.iter("RR"):
            tmpRRList.append(int(rr.text))
        oneMeasurement.addRRListToMeasurement(preprocessRR(tmpRRList))


        for acc in m.iter("Acceleration"):
            oneAcc = re.split(r';', acc.text)
            for coordinates in oneAcc:
                pos = re.findall(r'\-?[0-9]+', coordinates)
                if pos:
                    oneMeasurement.addACCListToMeasurement(Coordinates(int(pos[0]), int(pos[1]), int(pos[2])))

        for m_info in m.iter("StartDate"):
            sd=m_info.text

        for m_info in m.iter("StartTime"):
            st=m_info.text
        startdatetime = sd + " " + st
        t = oneMeasurement.measurement_start_time(startdatetime)
        res = t + timedelta(seconds=0.08)
        print(res)
        person.add_measurement(oneMeasurement)
        person.print_person_info()
        personInfo.append(person)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    personInfo = list()
    setVariablesFromXml(personInfo)
    #plotDiffRR(personInfo[0].measurements[0].rrList[0])
    # plotMovements(personInfo[0].measurements[0].accList)
    #featureRRplots(personInfo[0].measurements[0].rrList[0])

    # df = personInfo[0].measurements[1].getProcessedAcc()
    # plot_together(personInfo[0].measurements[1].rrList[0], df)

    accDF = personInfo[0].measurements[0].getDFacceleration()
    plot_together(personInfo[0].measurements[0].rrList[0], accDF)
    print(accDF.head())
    #personInfo[0].measurements[0].accelerationToCSV('src/coordinates.csv')

    #fftCoordinates(accDF)

    #rrFeatureExtraction(personInfo[0].measurements[0].rrList[0])
