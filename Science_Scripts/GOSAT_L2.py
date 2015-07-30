import os
import h5py
import math 

#default root path
DEFAULT_PATH = "//home//bama4//GOSAT_L2_Data"
EXT = ".h5"
XCO2_ARRAY_SIZE = 36

#constants for converting deg to km 
KM_LAT = 110.57
KM_LONG = 111.32

DEG_LAT_RANGE = 2.4
DEG_LONG_RANGE = 10.0

#returns date
def getDate(f):

    try:
        return f["Global"]["MD_Metadata"]["dateStamp"][0]
    except StandardError:
        return "ERROR: Invalid access"

#returns an array of XCO2 files
def getXCO2Array(f):

    xco2_array = []
    tmp_array = []

    for i in range(len(f["Data"]["mixingRatio"]["XCO2"])):
        tmp_array.append(f["Data"]["mixingRatio"]["XCO2"][i])
                
    try:
        return tmp_array
    except StandardError:
        return "ERROR: Invalid access"
     
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
    return km/KM_LONG

#check if given latitude is valid
def isValidLat(lat):
    return (lat >= -90.0 and lat <= 90.0)

#check if given longitude is valid
def isValidLong(lon):
    return (lon >= -180.0 and lon <= 180.0)

#obtain raw latitudes
def getRawLat(data_file):
    S_M = data_file["Data"]["geolocation"]
    LATS = S_M["latitude"]

    return LATS

#obtain raw longitudes
def getRawLong(data_file):
    S_M = data_file["Data"]["geolocation"]
    LONGS = S_M["longitude"]

    return LONGS

#ask if want to print obj (list,string, etc)
def prompt_print(msg,obj):
    ans = input(msg)
    if(ans == "y"):
        print(obj)
    else:
        return

#Is date a match to file 
def isFileDateMatch(file_name, date):
    if(date == ""):
        return True

    if(file_name.find(date) == -1):
        return False
    else:
        return True

#find specific files by their coordinates (with optional specified date
#Return file names, file objects, and the coordinates that are within the 
#range of the given center coordinate
def findFilesByCoords(start_dir,long_,lat_, date):

    fils = []
    fil_names = []
    coords = []
    type_co2 = []

    bound_lat_= input("Enter latitude bound: ")
    bound_long_ = input("Enter longitude bound: ")

    #go through files
    for f in start_dir.files:
        
        isInFile = False
        if(f.name[-len(EXT):] == EXT and isFileDateMatch(f.name,date)):
            file_obj = h5py.File(f.path,"r")
            
            #get longitudes and latitudes
            lat_raw = getRawLat(file_obj)
            long_raw = getRawLong(file_obj)
             
            for i in range(len(lat_raw)):
                if ( isInBound(lat_,bound_lat_,lat_raw[i]) ):
                    if (isInBound(long_,bound_long_,long_raw[i])):
                        coords.append(  (lat_raw[i],long_raw[i]) )
                        type_co2.append(getXCO2Array(file_obj)[i])
                             
                        if(isInFile == False):
                            fil_names.append(f.name)
                            fils.append(file_obj)
                            isInFile = True

    
    print("Results: ")
    print("fils length: " + str(len(fils)) + "fil_names length: " + str(len(fil_names)) + "coords length: " + str(len(coords))) + "type_co2 length: " + str(len(type_co2))

    return (fils, fil_names, coords, type_co2)


#Check if the two points/numbers are within the given range (num1 to num1-range_)
def isInRange(num1,num2,range_):
    p1 = num1
    p2 = num1-range_
    if (num2 >= 0):#pos coords
        if(num2 <= p1 and num2 >= p2):
            return True
        return False
    else:#neg coords
        p2 = num1+range_
        if(num2 >= p1 and num2 <= p2):
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
        

#avg data in list
def averageCO2(lst):
    
    avg = 0.0
    for i in range(len(lst)):
        avg = avg + lst[i]
    return avg/len(lst)

