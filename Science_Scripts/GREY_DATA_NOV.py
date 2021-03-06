import os 
import sys
import netCDF4

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


def storeMatchingPoints(files,coords):


   thread_lst = []


   for f in files:
      try:

          lats = getRawLat(f)

          longs = getRawLong(f)

          t = threading.Thread(target=searchArray, args=(lats,longs,coords,f,))
            
          thread_lst.append(t) 
          t.start()
          t.join()
            
      except:
          print("threading error for thread ")
          return
      print("Thread " + str(f) + " done.")


def searchArray(lat_raw,long_raw,coords,file_obj):

    print(coords)
    thread_lst = []
    try:
        for k in range(len(coords)):
            for j in range(1,NUM_THREADS+1):
                beg_ = len(lat_raw)*(j-1)
                end_= NUM_THREADS
                beg2_ = len(lat_raw)*(j)
                t = threading.Thread(target=getMatchCoord, args=(file_obj,coords[k],lat_raw[(beg_/end_):(beg2_/end_)],long_raw[(beg_/end_):(beg2_/end_)],)) 

                thread_lst.append(t)
                t.start()
                t.join()

    except KeyError:

        print("Error: exiting now")
        sys.exit(1)
    return


def getMatchCoord(file_obj,coords, lat_raw, long_raw):
 #are coords in range
    for i in range(len(lat_raw)):
        for j in range(len(lat_raw[i])):#avoiding having to indent everything again
            if ( isInRange(coords[LAT],lat_raw[i][j], kmTodegLat(KM_LAT_RANGE) )):
                if (isInRange(coords[LONG],long_raw[i][j],kmTodegLong(KM_LONG_RANGE)) ):
                    co2 = getRawCO2Flux(file_obj)[i][j]
                    MATCHING_POINTS.append(  (lat_raw[i][j],long_raw[i][j],co2) )
                    print("Point " + str( (lat_raw[i][j],long_raw[i][j],co2) ) + " added.")
            #print("On Current Coord: " + str(coords[k]))

    

#find raw coords and files
def findRawFilesByRawCoords(start_dir,coords):
    
   files = start_dir.returnAllFiles()
   f_nc4 = []

#get .h5 files
   for f in files:
      if(f.name[-len(EXT):] == EXT):
         f_nc4.append(netCDF4.Dataset(f.path,"r"))
   storeMatchingPoints(f_nc4,coords)
   return MATCHING_POINTS


#find specific files by their coordinates (with optional specified date
#Return file names, file objects, and the coordinates that are within the 
#range of the given center coordinate
def findFilesByCoords(start_dir,long_,lat_, date):

    fils = []
    fil_names = []
    coords = []
    type_co2 = []
    times = []
    
    bound_lat_=0
    bound_long_=0

    file_obj = None
    
    range_ = input("Use default range method?")
    

    #prompt for bounds
    if(range_ != "y"):
        bound_lat_= input("Enter latitude bound: ")
        bound_long_ = input("Enter longitude bound: ")
    
    


    for f in start_dir.files:
        
        isInFile = False
        
        try:
            file_obj = netCDF4.Dataset(f.path,"r")
        except:
            print("FILE: " + str(f.name) + " had an error")
            continue

       
        try:
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
                                type_co2.append( getRawCO2Flux(file_obj)[i][j] )
                            
                                print("POINT ADDED.")
                                
                                
                                if(isInFile == False):
                                    fil_names.append(f.name)
                                    fils.append(file_obj)
                                    isInFile = True
                                
            else: #custom range method
                
                    for i in range(len(lat_raw)):
                        for j in range(len(lat_raw[i])):
                            if ( isInBound(lat_,bound_lat_,lat_raw[i][j]) ):
                                if (isInBound(long_,bound_long_,long_raw[i][j])):
                                    coords.append(  (lat_raw[i],long_raw[i][j]) )
        
        
                                    #CO2 Levels
                                    type_co2.append( getRawCO2Flux(file_obj)[i][j] )
                                    print("POINT ADDED.")
                                    
                                    if(isInFile == False):
                                        fil_names.append(f.name)
                                        fils.append(file_obj)
                                        isInFile = True
    
        except:
            print("error in file " + str(f.name))
            continue
    return (fils, fil_names, coords, type_co2, times)
   

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
        











