import os
import sys
import netCDF4
import math 

DEFAULT_PATH_TW = "C://Users//Bama4//Downloads//DATA//FLUXNET_DATA//Twitchell California"
EXT = ".nc"


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

#check if water present
def isWater(w):
    return (WATER == w)


#check if given latitude is valid
def isValidLat(lat):
    return (lat >= -90.0 and lat <= 90.0)

#check if given longitude is valid
def isValidLong(lon):
    return (lon >= -180.0 and lon <= 180.0)

#Return years array
def getYears(data_file):
    YEARS = data_file.variables["YEAR"]
    return YEARS
    
def getDays(data_file):
    DOY = data_file.variables["DOY"]
    return DOY

#get strong CO2
def getRawCO2(data_file):

    co2_readings = data_file.variables["CO2"]
    
    return co2_readings

def getCO2Flux(data_file):

    flux = data_file.variables["FC"]
    return flux
    
#ask if want to print obj (list,string, etc)
def prompt_print(msg,obj):
    ans = input(msg)
    if(ans == "y"):
        print(obj)
    else:
        return

#Is FID a match to file 
def isFileMatch(file_name, reg):
    if(reg == ""):
        return True

    if(file_name.find(reg) == -1):
        return False
    else:
        return True

#gets CO2 data by date in format yyyymm
def findCO2ByDate(dir_, date):
    
    fils = []      #file objects
    fil_names = [] #file names
    coords = []    #coordinate names
    type_co2 = []  #CO2 values
    times = []     #times as [yyyy, mm , dd , hh , min , sec]
    
    file_obj = None

    for f in start_dir.files:
        
        isInFile = False
        
        try:
            file_obj = netCDF4.Dataset(f.path,"r")
        except:
            print("FILE: " + str(f.name) + " had an error")
            continue
            
        #make sure year matches
        if(isFileMatch(f.name,date[:4]) == False):
            continue
        
        f_day = getDays(file_obj)
        f_year = getYears(file_obj)
        f_data = getRawCO2()
        
        

#Check if the two points/numbers are within the given range (num2 to num2-range_)
#Where num2 are the raw points
def isInRange(num1,num2,range_):
    p1 = num2
    p2 = num2-range_
    
    #print("BEGIN " + str(num2) + " END " + str(p2))
    if (num1 >= 0):#pos coords
        if(num1 <= p1 and num1 >= p2):
            return True
        return False
    else:#neg coords
        p2 = num2+range_
        if(num1 >= p1 and num1 <= p2):
            return True
        return False

#check if the pt is in bounds between n1 and n2
def isInBound(n1,n2,pt):
    
    beg=0
    end=0

    #make sure grater number is on the left
    if(n1 >= n2):
        beg = n1
        end = n2
    else:
        beg = n2
        end = n1

    if(pt <= beg and pt >= end):
        return True
    return False
        


def avg_lst(lst):
    

    avg = 0.0
    for i in range(len(lst)):
        avg = avg + lst[i]
    return avg/len(lst)
