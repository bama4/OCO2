import os
import sys
import netCDF4
import math 

DEFAULT_PATH_TW = "C://Users//Bama4//Downloads//DATA//FLUXNET_DATA//Twitchell California"
EXT = ".nc"

LAT = 38.1087
LONG = -121.653

YEAR = 0
MONTH = 1
DAY = 2

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

#converts DOY parameter to month numbered 1 - 12 and day in format [yyy,m,dd]
#currently only accepts non-leap years
#rturns -1 if invalid doy
def doyToMonth(doy,year):
    
    if(year % 4 != 0):
        
        #january
        if(doy >=1 and doy <= 31):
            return [year,1,doy]
        
        #febuary
        if( (doy >= 32 and doy <= 59)):
            return [year,2,doy - 31]
        
        #march
        if(doy >= 60 and doy <= 90):
            return [year,3,doy - 59]
        
        #april
        if(doy >= 91 and doy<= 120):
           return [year,4,doy - 90]
            
        #may
        if(doy >= 121 and doy<= 151):
            return [year,5,doy - 120]

        #june
        if(doy >= 152 and doy <= 181):
            return [year,6,doy - 151]
            
        #july
        if(doy >= 182 and doy <= 212):
            return [year,7,doy - 181]
            
        #august
        if(doy >= 213 and doy <= 243):
            return [year,8,doy - 212]
            
        #september
        if(doy >= 244 and doy <= 273):
            return [year,9,doy - 243] 
            
        #october
        if(doy >= 274 and doy <= 304):
            return [year,10,doy - 273]
            
        #november
        if(doy >= 305 and doy <= 334):
            return [year,11,doy - 304]
        
        #december
        if(doy >= 335 and doy <= 365):
            return [year,12,doy - 334]
        print("NO MATCHING MONTH")
    else: #leap year
        #code for leap year here
        print("LEAP YEAR")
        pass
            
            
#gets CO2 data by date in format yyyymm
def findCO2ByDate(s_dir, date):
    
    fils = []      #file objects
    fil_names = [] #file names
    coords = []    #coordinates as (x,y)
    type_co2 = []  #CO2 values
    times = []     #times as [yyyy, mm , dd , hh , min , sec]
    
    file_obj = None

    for f in s_dir.files:
        
        isInFile = False
        
        try:
            file_obj = netCDF4.Dataset(f.path,"r")
        except:
            print("FILE: " + str(f.name) + " had an error")
            continue
            
            
        f_day = getDays(file_obj)
        f_year = getYears(file_obj)
        f_data = getRawCO2(file_obj)
        
        #make sure year matches
        if(int(date[:4]) != f_year[YEAR]):
            print("FILE YEAR DOES NOT MATCH GIVEN YEAR")
            print(date[:4] + " " + str(f_year[YEAR]))
            continue
        
       # try:

    
        for i in range(len(f_data)):
            
            #check if month matches
            if( int(date[2:]) == doyToMonth(f_day[i],int(date[:4]))[MONTH]):
                fils.append(file_obj)
                fil_names.append(f.name)
                type_co2.append(f_data[1])
                times.append( doyToMonth(f_day[i],int(date[:4])) )
                coords.append((LAT,LONG))
                print("DATA ADDED")
       # except:
           # print("AMERIFLUX DATASET ERROR")
    
    print("AMERIFLUX DATA OBTAINED")
    
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
        


def avg_lst(lst):
    

    avg = 0.0
    for i in range(len(lst)):
        avg = avg + lst[i]
    return avg/len(lst)
