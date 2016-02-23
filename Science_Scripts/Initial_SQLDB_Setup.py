import mysql.connector as SQL
import OCO2_Driver as Handle

import h5py
import os
import VFS
import sys
import OCO2_L1B
import OCO2_LITE
import OCO2_L2
import GREY_DATA_NOV
import AMERIFLUX_L2_STD

#initial format [[file_obj], [file_names], [coords], [data], [times])]
#adds to database
def addData(cnx,FILE,site_name):
    cursor = cnx.cursor()
    cursor.execute("USE sciencedata")
    
    for i in range (len(FILE[Handle.FILE_COORDS])):
        times = FILE[Handle.FILE_TIMES][i]
        add_record = ("INSERT INTO sites (Name, Longitude, Latitude, DATA_VAL, YEAR, MONTH, DAY ) VALUES (%s,%s,%s, %s, %s, %s, %s)")
        add_dat = (site_name , float(FILE[Handle.FILE_COORDS][i][1]) , float(FILE[Handle.FILE_COORDS][i][0]) , float(FILE[3][i]) , int(times[0]) , int(times[1]) , int(times[2]))
        
        try:
            cursor.execute(add_record, add_dat)
            cnx.commit()
        except Exception:
            print(add_record + " " + str(add_dat) + " CAUSED THE ERROR")
        
    pass
    
    
def main():
    
    #connect to data base
    cnx = SQL.connect(user='root', database='sciencedata', password='123')
    
    
    #create Ameriflux entries
    # Handle.getRoot()
    # Handle.CURR_DIR = Handle.FILE_SYS.root
    # files = AMERIFLUX_L2_STD.findCO2ByDate(Handle.CURR_DIR, "201412")
    # addData(cnx,files,"Ameriflux_TW")
    # print("Data Complete")
    # Handle.FILE_SYS = 0
    # Handle.CURR_DIR = 0
    
    #create OCO2_LITE Barrow entries
    # Handle.getRoot()
    # Handle.CURR_DIR = Handle.FILE_SYS.root
    # long_ = input("Enter longitude.")
    # lat_ = input("Enter Latitude.")
    # files =  OCO2_LITE.findFilesByCoords(Handle.CURR_DIR, long_, lat_,"")
    # addData(cnx,files,"OCO2_Barrow")
    # print("Data Complete")
    # Handle.FILE_SYS = 0
    # Handle.CURR_DIR = 0
    
    #create OCO2_LITE Twitchell entries
    # Handle.getRoot()
    # Handle.CURR_DIR = Handle.FILE_SYS.root
    # long_ = input("Enter longitude.")
    # lat_ = input("Enter Latitude.")
    # files =  OCO2_LITE.findFilesByCoords(Handle.CURR_DIR, long_, lat_,"")
    # addData(cnx,files,"OCO2_Twitchell")
    # print("Data Complete")
    # Handle.FILE_SYS = 0
    # Handle.CURR_DIR = 0
    
    #create OCO2_LITE Fort Peck entries
    # Handle.getRoot()
    # Handle.CURR_DIR = Handle.FILE_SYS.root
    # long_ = input("Enter longitude.")
    # lat_ = input("Enter Latitude.")
    # files =  OCO2_LITE.findFilesByCoords(Handle.CURR_DIR, long_, lat_,"")
    # addData(cnx,files,"OCO2_FortPeck")
    # print("Data Complete")
    # Handle.FILE_SYS = 0
    # Handle.CURR_DIR = 0
    
    #create OCO2_LITE Fort Peck entries
    # Handle.getRoot()
    # Handle.CURR_DIR = Handle.FILE_SYS.root
    # long_ = input("Enter longitude.")
    # lat_ = input("Enter Latitude.")
    # files =  OCO2_LITE.findFilesByCoords(Handle.CURR_DIR, long_, lat_,"")
    # addData(cnx,files,"OCO2_K34")
    # print("Data Complete")
    # Handle.FILE_SYS = 0
    # Handle.CURR_DIR = 0
    
    #create OCO2_World entries
    Handle.getRoot()
    Handle.CURR_DIR = Handle.FILE_SYS.root
    long_ = input("Enter longitude.")
    lat_ = input("Enter Latitude.")
    files =  OCO2_LITE.findFilesByCoords(Handle.CURR_DIR, long_, lat_,"")
    print("Adding data now...")
    addData(cnx,files,"OCO2_World")
    print("Data Complete")
    Handle.FILE_SYS = 0
    Handle.CURR_DIR = 0
    
main()
