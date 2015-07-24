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
    
    Methods:
        
        
    


#############################################################   O  C  O  2 _ L  1  B  .  P   Y   ######################################################


