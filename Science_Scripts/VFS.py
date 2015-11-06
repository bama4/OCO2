#Mariama Barr - Dallas
#1/11/2015
#
#VFS.py
#Description: This package is an implentation of a virtual file system that creates 
#itself based upon the current given directory
import os
import h5py
import OCO2_L1B
import OCO2_LITE
import OCO2_L2
import math 

CURR_DIR_ = 0
SUB_DIR = 1
FILES = 2
EXT = ".h5"
EXT2 = ".nc4"
EXT3 = ".nc"

#Extra class
class Node:
    
    def __init__(self,label,obj):
        self.label = label
        self.obj = obj
        

#File object ( name , pathname )
class File:
    
    
    #init constructor
    def __init__(self,name,path):
        self.name = name
        self.path = path
    
    #print files
    def print_f(self):
        print("NAME: " + self.name + " PATH: " + self.path)

#Directory object ( name , pathname , [Directories] , [Files]) 
class Directory:
    
    #init constructor
    def __init__(self,name,path,subdirs, files):
        self.name = str(name)
        self.path = path
        self.subdirs = subdirs
        self.files = files
    
    #print directory
    def print_d(self):
        print(" NAME: " + self.name + " PATH: " + self.path)
        print("DIRECTORIES")
        
        for dir_ in self.subdirs:
            print(dir_.name)
        
        print("\nFILES")
        
        for f in self.files:
            f.print_f()
            
            
    #Returns array of child subdirectories        
    def getSubDirs(self):
        return self.subdir
            
    #Returns a directory based on the given name        
    def getSubDir(self,name):
        
        for dir_ in self.subdirs:
            print(self.name)
            if(dir_.name == name):
                return dir_
            else:
                continue
        return None  
        
    #Returns the list of Files in the Directory
    def getFiles(self):
        return self.files

    #Returns a File by name in the Directory
    #Or sub directories
    def getFile(self,name):
        
        for file_ in self.files:
            if(file_.name == name):
                return file_
        return None
    
    #Adds a directory object to list of subdirectories
    def addDir(self,dir_):
        self.subdirs.append(dir_)
        
    #Adds a File object to list of files
    def addFile(self,f):
        self.files.append(f)
        
    #return files
    def returnAllFiles(self):
        
        files = []

        #get this directorys files
        for fi in self.getFiles():
            files.append(fi)

        #get all directories of root file
        for d in self.subdirs:
            for f in d.getFiles():
                files.append(f)
        return files
        
#Virtual File System (VFS) object class        
class VFS:
    
    
    def __init__(self,name,path,root):
        self.name = name
        self.path = path
        self.root = root #directory chain
        
    #Print VFS 
    def print_VFS(self):
        
        print("NAME: " + self.name + " PATH: " + self.path)
        self.root.print_d()
        
    #Return root directory
    def getDir(self):
        return self.root
   
    #find given directory
    def findD(self,name,dirs):
        
        d = None
          
        for dir_ in dirs:
            if(dir_.name == name):
                #print("FOUND")
                return dir_
                
            d = dir_.getSubDir(name)
            if(d != None):
                print("FOUND")
                break;
            else:
                return self.findD(name, dir_.subdirs)
        
        return d
    
    #find given directory        
    def findDir(self,name):
        return self.findD(name,[self.root])

   
    
    
    #Set up VFS with directories and files
    def addDirs(self,root,path):
    
    #     print("CURRENT PATH: " + path)
    #     print("CURRENT DIRECTORY: " + root.name)
    #     
    #  
        
        walker = os.walk(path)
        
        for curr in walker:
            root.name = str(curr[CURR_DIR_].split("//")[-1])
            root.path = curr[CURR_DIR_]
    
            #set up file info
            #only collect .h5 files
            for f in curr[FILES]:
                if(f[-len(EXT):] == EXT or f[-len(EXT2):] == EXT2 or f[-len(EXT3):] == EXT3):
                    root.files.append(File(f,curr[CURR_DIR_]+"//"+f))
                
            #set up sub-directories
            
            for i in curr[SUB_DIR]:
                
                dir_ = Directory(i , curr[CURR_DIR_]+"//"+i, [] , [] )
                root.subdirs.append(dir_)
                
    #             print("CURRENT PATH: " + path)
    #             print("CURRENT DIRECTORY: " + root.name)
    #             
    #             print("PATH: " + dir.path)
    #             print("DIRECTORY: " + dir.name)
                self.addDirs(dir_, dir_.path)
            break
            
    #Add directories and files to VFS recursively  
    def setVFS(self,root_path):
    
        root_d= Directory(str(root_path.split("//")[-1]), root_path, [], [])
        self.root = root_d
        self.path = root_path
        
        #FILE_SYS.print_VFS()
        self.addDirs(root_d, root_path)
        
