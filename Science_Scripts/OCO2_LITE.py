import threading
import os
import sys
import h5py
import math 


#default root path
DEFAULT_PATH = "//home//bama4//OCO2_L2_LITE_DATA//Data"
EXT = ".nc4"

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
    S_M = data_file["SoundingGeometry"]
    LATS = S_M["sounding_latitude"]

    avg_lat = []
    counter = 0
    for i in range(len(LATS)):
        avg = 0.0
        
        for j in range(len(LATS[i])):

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

    S_M = data_file["SoundingGeometry"]
    LONGS = S_M["sounding_longitude"]

    avg_long = []
    counter = 0
    for i in range(len(LONGS)):
        avg = 0.0

        for j in range(len(LONGS[i])):
            #make sure latitude is valid
            if(isValidLong(LONGS[i][j])):
                avg = avg + LONGS[i][j]
                counter = counter + 1
        if(counter !=0):        
            avg_long.append(avg/counter)
            counter = 0
    return avg_long


#get strong CO2
def getRawCO2(data_file):
    
    co2_readings = data_file["xco2"]
    
    return co2_readings

#get weak CO2
def getRawCO2Weak(data_file):
    
    S_M = data_file["SoundingMeasurements"]
    co2_readings = S_M["radiance_weak_co2"]
    return cos_readings

#obtain raw latitudes
def getRawLat(data_file):
    LATS = data_file["latitude"]
    return LATS

#obtain water indicator array
def getWaterArray(data_file):
    WAT = data_file["land_water_indicator"]
    return WAT

#obtain raw longitudes
def getRawLong(data_file):
    LONGS = data_file["longitude"]
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


def storeMatchingPoints(files,coords):


   thread_lst = []


   for f in files:
      try:

          lats = getRawLat(f)
          print("FGFG")
          print(str(lats))
          longs = getRawLong(f)
          water = getWaterArray(f)

          t = threading.Thread(target=searchArray, args=(lats,longs,water,coords,f,))
            
          thread_lst.append(t) 
          t.start()
          t.join()
            
      except:
          print("threading error for thread ")
          return

 
      print("Thread " + str(f) + " done.")


def searchArray(lat_raw,long_raw,water_lst,coords,file_obj):

    print(coords)
    thread_lst = []
    try:
        for k in range(len(coords)):
            for j in range(1,NUM_THREADS+1):
                beg_ = len(lat_raw)*(j-1)
                end_= NUM_THREADS
                beg2_ = len(lat_raw)*(j)
                t = threading.Thread(target=getMatchCoord, args=(file_obj,coords[k],lat_raw[(beg_/end_):(beg2_/end_)],long_raw[(beg_/end_):(beg2_/end_)],water_lst[(beg_/end_):(beg2_/end_)],)) 

                thread_lst.append(t)
                t.start()
                t.join()

    except KeyError:

        print("Error: exiting now")
        sys.exit(1)
    return


def getMatchCoord(file_obj,coords, lat_raw, long_raw, water_lst):
 #are coords in range
    for i in range(len(lat_raw)):
        if(True):#avoiding having to indent everything again
            if ( isInRange(coords[LAT],lat_raw[i], kmTodegLat(KM_LAT_RANGE) ) and isWater(water_lst[i]) == False):
                if (isInRange(coords[LONG],long_raw[i],kmTodegLong(KM_LONG_RANGE)) ):
                    co2 = getRawCO2(file_obj)[i]
                    MATCHING_POINTS.append(  (lat_raw[i],long_raw[i],co2) )
                    print("Point " + str( (lat_raw[i],long_raw[i],co2) ) + " added.")
            #print("On Current Coord: " + str(coords[k]))

    

#find raw coords and files
def findRawFilesByRawCoords(start_dir,coords):
    
   files = start_dir.returnAllFiles()
   f_h5 = []
	
#get .h5 files
   for f in files:
      if(f.name[-len(EXT):] == EXT):
         f_h5.append(h5py.File(f.path,"r"))
	 print(f.name)
   storeMatchingPoints(f_h5,coords)
   return MATCHING_POINTS
	    

#find specific files by their coordinates (with optional specified date
#Return file names, file objects, and the coordinates that are within the 
#range of the given center coordinate
def findFilesByCoords(start_dir,long_,lat_, date):

    fils = []
    fil_names = []
    coords = []
    type_co2 = []

    bound_lat_=0
    bound_long_=0

    avg_ = input("Average the Data?")
    range_ = input("Use default range method?")
    co2_ = input("Include strong CO2 's' or weak CO2 'w'?")

    #prompt for bounds
    if(range_ != "y"):
        bound_lat_= input("Enter latitude bound: ")
        bound_long_ = input("Enter longitude bound: ")



    for f in start_dir.files:
        
        isInFile = False
        if(f.name[-len(EXT):] == EXT and isFileDateMatch(f.name,date)):
            file_obj = h5py.File(f.path,"r")
                
            #Ask if data should be averaged
            if(avg_ == "y"):
                lat_avg = getLatAvg(file_obj) 
                long_avg = getLongAvg(file_obj)

            #prompt to print averages
            #prompt_print("Would you like to print the latitude averages for file " + str(f.name)+ str("?"),lat_range)
            #prompt_print("Would you like to print the longitude averages for file " + str(f.name)+ str("?"),long_range)
            
                print("Finished calculating averages for file " + str(f.name))
                isInFile = False

            #are coords in range

                if(range_ == "y"): #default range method
                    for i in range(len(lat_avg)):
                        if ( isInRange(lat_,lat_avg[i],DEG_LAT_RANGE) ):
                        
                            if (isInRange(long_,long_avg[i],DEG_LONG_RANGE)):
                                coords.append(  (lat_avg[i],long_avg[i]) )


                                
                                if(isInFile == False):
                                    fil_names.append(f.name)
                                    fils.append(file_obj)
                                    isInFile = True

                else: #custom range method
                    for i in range(len(lat_range)):
                        if ( isInBound(lat_,bound_lat_,lat_avg[i]) ):

                            if (isInRange(long_,bound_long_,long_avg[i])):
                                coords.append(  (lat_avg[i],long_avg[i]) )

                                if(isInFile == False):
                                    fil_names.append(f.name)
                                    fils.append(file_obj)
                                    isInFile = True


            #get coords using raw data
            else:

                lat_raw = getRawLat(file_obj)
                long_raw = getRawLong(file_obj)
                print("Finished obtaining raw longitude and latitude for file " + str(f.name))
    
                #are coords in range

                if(range_ == "y"):#default range method
                    for i in range(len(lat_raw)):
                        for j in range(len(lat_raw[i])):
                            if ( isInRange(lat_,lat_raw[i][j],DEG_LAT_RANGE) ):
                                if (isInRange(long_,long_raw[i][j],DEG_LONG_RANGE)):
                                    coords.append(  (lat_raw[i][j],long_raw[i][j]) )


                                                                    #CO2 Levels
                                    if(co2_ == "s"): #strong
                                        type_co2.append( averageCO2(getRawCO2Strong(file_obj)[i][j]) )

                                    if(co2_ == "w"): #weak
                                        type_co2.append( averageCO2(getRawCO2Weak(file_obj)[i][j]) )


            
                                    if(isInFile == False):
                                        fil_names.append(f.name)
                                        fils.append(file_obj)
                                        isInFile = True
                else: #custom range method
                    
                     for i in range(len(lat_raw)):
                        for j in range(len(lat_raw[i])):
                            if ( isInBound(lat_,bound_lat_,lat_raw[i][j]) ):
                                if (isInBound(long_,bound_long_,long_raw[i][j])):
                                    coords.append(  (lat_raw[i][j],long_raw[i][j]) )


                                                                      #CO2 Levels
                                    if(co2_ == "s"): #strong
                                        type_co2.append( averageCO2(getRawCO2Strong(file_obj)[i][j]) )

                                    if(co2_ == "w"): #weak
                                        type_co2.append( averageCO2(getRawCO2Weak(file_obj)[i][j]))


                                    if(isInFile == False):
                                        fil_names.append(f.name)
                                        fils.append(file_obj)
                                        isInFile = True



    return (fils, fil_names, coords, type_co2)

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
        

#avg data in list
def averageCO2(data_file):
    
    S_M = data_file["SoundingMeasurements"]
    co2_readings = S_M["radiance_strong_co2"]

    lst = []
    tmp_lst = []
    for i in range(len(co2_readings)):
        tmp_lst.append([avg_lst(co2_readings[i][0])])
        for j in range(1,len(co2_readings[i])):
            tmp_lst[i].append(avg_lst(co2_readings[i][j]))
            
    return tmp_lst
    
def avg_lst(lst):
    

    avg = 0.0
    for i in range(len(lst)):
        avg = avg + lst[i]
    return avg/len(lst)

    
#raw co2 to xco2 (air molar fraction)
def rawCO2ToXCO2(lst):
    pass

