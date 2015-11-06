import h5py
import os
import VFS
import sys
import OCO2_L1B
import OCO2_LITE
import OCO2_L2
import GREY_DATA_NOV

COMMANDS = ["Create VFS from root directory","Set Current Directory", "List files of Current Directory","Open/Set File In Current Directory" , "List Groups", "List DataSets", "Display BUFFER Contents","Print Contents of Current Directory","Flush Buffer","Put Files With Coord Range In Buffer","Display DataSet for Current File","Put Files in bound In Buffer","Output Data To File","Display long. average", "Display lat. average", "Run Automatic Script Given file, get all Coords. within a certain point(OCO2_L1B , OCO2_L2 , OCO2_LITE)."]

PATH = ""
SYS_NAME = "OCO2_DATA_FILES"
FILE_SYS = VFS.VFS(SYS_NAME,None,None)
CURR_DIR = None
CURR_FILE = None

BUFFER = []
EXIT = 99

#HAMSTERMAP PARAMETERS
HAM_MARKER = "circle1"
HAM_COLOR = "yellow"
HAM_LEGEND = "Level1B Points"

#GOOGLE MAP PARAMETERS


#check for valid input
def isValidInput(inp):
    
    isValid = False
    isValid = (type(inp) == int)
    if (inp == EXIT):
        return True
    
    for i in range(len(COMMANDS)):
        isValid = (inp == i)
        if(isValid == True):
            break
    return isValid



#getinput
def getInput():
    
    isValid = False
    isExit = False
    
    c = -1
    while(not(isValid) and not(isExit)):
        print("Enter one of the following commands or press '99' to exit")
        displayMenu()
    
        #make sure c is of type 'int'
        try:
            c = int(input())
        except StandardError:
            print("Invalid Coomand")
            isValid = False
        isValid = isValidInput(c)
    return c    


#Get root path for file system
def getRoot():
    
    global FILE_SYS
    isValid = False
    ans = -1
    while(not(isValid)):
        
        ans = input("Enter root directory you would like the VFSto start from or enter " + str(EXIT) + " to exit")
        
        if(ans == EXIT):
            sys.exit(0)
            
        if(ans == "OCO2L1B"):
            ans = OCO2_L1B.DEFAULT_PATH
        elif(ans == "OCO2LITE"):
            ans = OCO2_LITE.DEFAULT_PATH
        elif(ans == "OCO2L2"):
            ans = OCO2_L2.DEFAULT_PATH
        elif(ans == "GREYDATANOV"):
            ans = GREY_DATA_NOV.DEFAULT_PATH
        try:
            
            os.chdir(ans)
            
        except StandardError:
            
            print("Directory does not exist")
            isValid = False
            return
            
        isValid = True
        
    FILE_SYS = VFS.VFS(SYS_NAME,ans,None)
    FILE_SYS.setVFS(ans)
 
#get the specified directory
def getDirectory():
    global FILE_SYS
    name = str(input("Enter name of Directory or type '_ROOT_' for ROOT dir as current dir"))
    
    if(name == "_ROOT_"):
        return FILE_SYS.root
    else:
        return FILE_SYS.findDir(name.strip())

#get the specified file
def getFile():
    
    global CURR_DIR
    name = str(input("Enter name of the file"))

    dir_f = CURR_DIR.getFile(name.strip())
    
    return dir_f

#display the menu
def displayMenu():
    
    for i in range(len(COMMANDS)):
        print(str(i) + " - " + COMMANDS[i])
    
#make sure file system/current directory is not "None'    
def checkFileSys():
    if(FILE_SYS == None):
        print("No file system has been created yet")
        return False
        
    if(CURR_DIR == None):
        print("There is no current directory set")
        return False
        
    return True
            
def getGroup():
    pass
    
def getDataSet():
    pass

def save(obj):
    
    global BUFFER
    BUFFER.append(obj)    

#file is in format NAME  LAT  LONG  TIMEOFFSET
#returns list of tuples of (NAME,LAT,LONG)
def getCoordsFromFile(name):

   try:
       f = open(name, 'r')
    
       coords = []
       lst = f.read().split("\n")
       for i in range(len(lst)):
           sublst = lst[i].split(" ")
           print(sublst)

           if(len(sublst)>=3):
               coords.append((sublst[0],float(sublst[1]),float(sublst[2])))
   except:
      print("GETCOORDSFROMFILE ERROR")

   return coords

#save names in buffer to text file
def saveToTextFile(name,lst):    
    global BUFFER

    f = open(name, 'w')
    for i in range(len(lst)):
        f.write(str(lst[i])+ str("\n"))
    f.close()

#converts coordinates to hamstermap format
def coordsToHamstermapFormat(coords,other):
    
    string_list = []
    LAT = 0
    LONG = 1
    CO2 = 0
    TIME = 1
 
    default_leg = input("Use default HAM_LEGEND for legend and default Number for Number? ")
    

    if(default_leg == "y"): #using default legend
        for i in range(len(coords)):
            string_list.append(str(coords[i][LAT])+str("\t")+ str(coords[i][LONG]) + str("\t") +str(HAM_MARKER) + str("\t") + str(HAM_COLOR) + str("\t") + str(i+1) + str("\t") + str(HAM_LEGEND)+ str("\n"))
    else: #use custom legend
        leg = input("Enter legend to use: ")
        for i in range(len(coords)):
            string_list.append(str(coords[i][LAT])+str("\t")+ str(coords[i][LONG]) + str("\t") +str(HAM_MARKER) + str("\t") + str(HAM_COLOR) + str("\t") + str(other[CO2][i]) + str("\t") + str(other[TIME][i]) + str(leg)+ str("\n"))

    return string_list



def saveCoordsToTextFile(name, formatted_list):
    f = open(name, "w")
    for i in range(len(formatted_list)):
        f.write(str(formatted_list[i]))
    f.close()

#where lst_tup is a list of (NAME , LAT, LONG)
def saveListTupleToFile(name, lst_tup):
    
    NAME = 0
    LAT  = 1
    LONG = 2

    try:

        f = open(name,"w")
        for i in range(len(lst_tup)):
            f.write(str(lst_tup[i][NAME]) + " " + str(lst_tup[i][LAT]) + " " + str(lst_tup[i][LONG]) + "\n")
        f.close()
    except:
        print("OCO2_ Driver error")
        sys.exit(1)

def procCommands(c):        
        global FILE_SYS
        global CURR_DIR
        global CURR_FILE
        global BUFFER
        
        if c == 0:
        
            
            getRoot()
            return 
            
        if c == 1: #set current directory
            
            checkFileSys()
            dir_ = getDirectory()
            if(dir_ == None):
                print("Directory does not exist")
            else:
                CURR_DIR = dir_
                
            return
            
           
        if c == 2: #Print files in current directory
            
            if(FILE_SYS == None):
                print("No file system has been created yet")
                return
                
            if(CURR_DIR != None):
                for f in CURR_DIR.files:
                    print(f.name)
            else:
                print("Current directory is not set")
                
            return
            
        if c == 3: #Set current file
            
            f = getFile()
            
            if(f != None):
                CURR_FILE = h5py.File(f.path,"r")
                save(CURR_FILE)
                
                print(f.name + " has been opened and set as CURR_FILE")
            else:
                print("File does not exist")
            return
            
            
        if c == 4: #display groups
            
            if(CURR_FILE == None):
                print("No file has been set")
                
            else:
                for group in CURR_FILE:
                    print(group)
            return
            
        if c == 5: #Display datasets
    
            checkFileSys()
            if(CURR_FILE == None):
                print("No file has been set")
                return
                
            name = input("Enter name of group to show names of datasets")
            d = None
            
            try:
                
                d = CURR_FILE[name]
                
            except StandardError:
                
                print("Invalid Group Name")
                return
            for data in d:
                print(data)
                
            return
            
        if c == 6: #Display BUFFER
            
            print("Contents of BUFFER")
            for thing in BUFFER:
                print(thing)
                
        if c == 7: #print current directory
            
            checkFileSys()

            if(CURR_DIR != None):
                CURR_DIR.print_d()
            else:
                print("Current directory not set")

        if c == 8: #Flush Buffer
            
            BUFFER[:] = []
            
        
        if c == 9: #place files in buffer given latitudes and longetudes
            lat_ = input("Enter the latitude you are looking for")
            long_ =  input("Enter the longitude longitude you are looking for")

            #optional date
            date = str(input("Enter the date as yymmdd(optional-enter 'n' otherwise)"))
            if(date == "n"):
                date = ""

            if(CURR_DIR == None):
                print("current directory has not been set")
                return 
                
            else:
                FILE_OBJS = 0
                FILE_NAME = 1
                FILE_COORDS = 2
                FILE_CO2_LEVELS = 3
                FILE_TIMES = 4

                nam = input("ENTER THE SOURCE (OCO2_L2 , OCO2_LITE, OCO2_L1B): ")
                #find the files with the correct coords (directory , longitude, latitude, optional date)
                
                if(nam == "OCO2_L2"):
                    files = OCO2_L2.findFilesByCoords(CURR_DIR, long_, lat_,date)
               
                elif(nam == "OCO2_L1B"):
                    files = OCO2_L1B.findFilesByCoords(CURR_DIR, long_, lat_,date)
                
                elif(nam == "OCO2_LITE"):
                    files = OCO2_LITE.findFilesByCoords(CURR_DIR, long_, lat_,date)
                elif(nam == "GREYDATANOV"):
                    files = OCO2_LITE.findFilesByCoords(CURR_DIR, long_,lat_,date)
                    
                #print file names
                print("The following files will be placed in the buffer: ")
                
                for i in range(len(files[FILE_NAME])):
                    print(files[FILE_NAME][i])
                    save(files[FILE_OBJS][i])
                #save(files[FILE_COORDS])

                #print points that fall in the coordinate range
                print("Number of points that fall in the region: " + str(len(files[FILE_COORDS])) )

                #write to file?
                ans = input("Write coords to file?")
                if(ans == "y"):
                    nam = input("Enter name of file: ")
                    saveCoordsToTextFile(nam,  coordsToHamstermapFormat(files[FILE_COORDS] ,[  files[FILE_CO2_LEVELS],files[FILE_TIMES] ] )  )
        
                else:
                    print("Not writing coords to file....")

                #write file names to file?
                ans = input("Write to file names that fall into the given bounding?")
                if(ans == "y"):
                    nam = input("Enter name of file: ")
                    saveToTextFile(nam,files[FILE_NAME])
                else:
                    print("Not writing file names to file...")

        if c == 10: #print data set
            
            if CURR_FILE == None:
                print("Current file not set")
                return
                
            group_n = input("Enter the Group name of this file")
            data_n  = input("Enter the data set name of this group")
            data_set = None
            
            try:
                
                data_set = CURR_FILE[group_n][data_n]
                
            except StandardError:
                
                print("Invalid Group Name")
                return

            for thing in data_set:
                print(thing)
            print("The following data set is " + str(len(data_set)) + str("rows long") + str(" and ") + str(len(data_set[0])) + str(" wide."))
            print("By " + str(len(data_set[0][0][0]))  )

        if c == 11: #return files that are within a certain km^2 with long,lat at the center
            pass
            
        if c == 12: #Output to file
            pass
            
        if c == 13: #Display long average of file
            if CURR_FILE == None:
                print("Current file not set")
                return

            print("Average longitude is : " + str(OCO2_L1B.getLongAvg(CURR_FILE)))

        if c == 14: #display lat. average of file
            if CURR_FILE == None:
                print("Current file not set")
                return

            print("Average latitude is : " + str(OCO2_L1B.getLatAvg(CURR_FILE)))

        if c == 15: #run automatic script
            
            try:

                n = input("Enter the file name containing the coords")
                coords = getCoordsFromFile(n)
                
                nam = input("ENTER THE SOURCE (OCO2_L2 , OCO2_LITE, OCO2_L1B): ")
                #find the files with the correct coords (directory , longitude, latitude, optional date)
                
                if(nam == "OCO2_L2"):
                    files = OCO2_L2.findRawFilesByRawCoords(CURR_DIR,coords)
                elif(nam == "OCO2_L1B"):
                    files = OCO2_L1B.findRawFilesByRawCoords(CURR_DIR,coords)
                elif(nam == "OCO2_LITE"):
                    files = OCO2_LITE.findRawFilesByRawCoords(CURR_DIR,coords)
                elif(nam == "GREYDATANOV"):
                    files = GREY_DATA_NOV.findRawFilesByRawCoords(CURR_DIR, coords)
                

        if c == EXIT:
            print("BYE")
            sys.exit(0)
            
def main():
    
    while(True):
        
        inp = getInput()
        procCommands(inp)
        print("\n\n\n")
        #FILE_SYS.print_VFS()
    print(inp)
    
    
main()
    
