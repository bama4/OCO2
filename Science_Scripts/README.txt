#Author: Mariama Barr - Dallas (2015)
#This file explains the OCO2 data set processor
#
#
#


#####################################################################   V  F  S   .  P   Y   ##########################################################
Description: 
VFS.py is a virtual file system that uses the following python packages:
- os  , h5py  , OCO2_L1B  , math

Objects: # The following objects are included in VFS
#File object ( name , pathname )
class File:
    
    Methods:
        #print files
        def print_f(self):
            
#Directory object ( name , pathname , [Directories] , [Files]) 
class Directory:
    
    Methods:
         #Returns array of child subdirectories        
        def getSubDirs(self):
        
        #Returns a directory based on the given name        
        def getSubDir(self,name):
    
        #Returns the list of Files in the Directory
        def getFiles(self):
            
        #Returns a File by name in the Directory
        #Or sub directories
        def getFile(self,name):
            
        #Adds a directory object to list of subdirectories
        def addDir(self,dir):
            
        #Adds a File object to list of files
        def addFile(self,f):
            
        
#Virtual File System (VFS) object class        
class VFS:
            
        
    


#############################################################   O  C  O  2 _ L  1  B  .  P   Y   ######################################################
Description:
OCO2_L1B.py is a module that contains the functions to access OCO2_L1B data.




#############################################################   O  C  O  2  _  D  R  I  V  E  R  .  P  Y  #############################################
Description:
OCO2_Driver.py is the main program that displays a menu of options to the user
Below are the following options in the program:

0 - Create VFS from root directory
1 - Set Current Directory
2 - List files of Current Directory
3 - Open/Set File In Current Directory
4 - List Groups
5 - List DataSets
6 - Display BUFFER Contents
7 - Print Contents of Current Directory
8 - Flush Buffer
9 - Put Files With Coord Range In Buffer
10 - Display DataSet for Current File
11 - Put Files in bound In Buffer
12 - Output Data To File
13 - Display long. average
14 - Display lat. average
15 - Run Automatic Script Given file, get all Coords. within a certain point


Functions:




Instructions:
-Regardless of option, must first select option '0' to establish the root directory,
  - 
-Then select option '1' to enter the current directory containing the files that you 
would like to work with.



