import os 
import sys

DEFAULT_PATH = "C://Users//Bama4//Downloads//DATA//GREY_DATA//DailyOutput_4Pierre"
EXT = ".nc"

#constants for converting deg to km 
KM_LAT = 110.574
KM_LONG = 111.32

DEG_LAT_RANGE = 2.4
DEG_LONG_RANGE = 10.0

KM_LAT_RANGE = 6 
KM_LONG_RANGE = 6

WATER = 1

NAME = 0
LAT = 1
LONG = 2

MATCHING_POINTS = []
NUM_THREADS = 50

#return coord of the given dataset
def processCoordDataSet(data_set):
    coord_c = int(len(data_set[0])/2)
    coord_r = int(len(data_set)/2)
        
    return data_set[coord_r][coord_c]
        
#converts latitude to km
def degLatToKm(deg):
    return deg*KM_LAT

#converts km to latitude
def kmTodegLat(km):
    return km/KM_LAT
    
#converts longetude to km
def degLongToKm(deg):
    return deg*KM_LONG
    
#converts km to latitude
def kmTodegLong(km):
    return km/(KM_LONG)

#converts moles to ppm
def molesToPPM(mol):
    return mol/pow(10,6)

#check if water present
def isWater(w):
    return (WATER == w)

#average latitude from file
def getLatAvg(data_file):
    
    LATS = data_file.variables["lat"]

    avg_lat = []
    counter = 0
    
    avg = 0.0
    
    for j in range(len(LATS)):

        #make sure longitude is valid
        if(isValidLat(LATS[i][j])):
            avg = avg + LATS[i][j]
            counter = counter + 1  
                  
    if(counter != 0):
        avg_lat.append(avg/counter)
        counter = 0
    return avg_lat


#check if given latitude is valid
def isValidLat(lat):
    return (lat >= -90.0 and lat <= 90.0)

#check if given longitude is valid
def isValidLong(lon):
    return (lon >= -180.0 and lon <= 180.0)

#average longitude from file
def getLongAvg(data_file):

    LONGS = data_file.variables["lon"]

    avg_long = []
    counter = 0
    
    avg = 0.0
    
    for j in range(len(LONGS)):

        #make sure longitude is valid
        if(isValidLat(LONGS[j])):
            avg = avg + LONGS[j]
            counter = counter + 1  
                  
    if(counter != 0):
        avg_long.append(avg/counter)
        counter = 0
    return avg_long


#get strong CO2
def getRawCO2Flux(data_file):
    
    co2_readings = data_file.variables["NEE_tavg"]
    return co2_readings

#obtain raw latitudes
def getRawLat(data_file):
    LATS = data_file.variables["lat"]
    return LATS

#obtain raw longitudes
def getRawLong(data_file):
    LONGS = data_file.variables["lon"]
    return LONGS

