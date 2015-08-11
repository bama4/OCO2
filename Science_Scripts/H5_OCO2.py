import h5py
import VFS
import OCO2_L1B
#For L1B Data for 2014 and 2015
ROOT_DIR = OCO2_L1B.DEFAULT_PATH
YEARS = [ "2014" , "2015" ]
EXT = ".h5"

#Set up Virtual File System for HDF5 Files
SYS_NAME = "2014 - 2015 HDF5 FILES"
FILE_SYS = VFS.VFS(SYS_NAME,ROOT_DIR,None)

#For transversing through  os.walk object



def main(): #test
    
    FILE_SYS.setVFS(ROOT_DIR)
    #FILE_SYS.print_VFS()
    print(FILE_SYS.findDir("348").files[0].name)
    print("IN PROGRESS")
    
    
    
main()
