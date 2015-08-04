import math
import numpy 

DEFAULT_FILE_NAME = "BARROW_JUNE1_POINTS.txt"

#opens the file
def getFile():

    try:
        ans = input("Please enter the file name: ")
        if(ans == "DEFAULT_FILE_NAME"):
            return open(DEFAULT_FILE_NAME,"r")
        else:
            return open(ans, "r")
    except StandardError:
        print("Invalid file name")
        return None

#Gets the coordinates and the "amount" column
#Returns an array of coords and their corresponding values as [ (X,Y,VALUE) , ... ]
def processFileAsHamText(file_):

    if(file_ == None):
        print("File is empty/File does not exist")
        return None

    #positions in the array
    X_COORD = 0
    Y_COORD = 1
    VALUE = 4
    
    coord_val_pairs = []
    tmp_array = []

    for line in file_:
        tmp_array = line.strip().split("\t")
        coord_val_pairs.append( (tmp_array[X_COORD], tmp_array[Y_COORD], tmp_array[VALUE]) )
    return coord_val_pairs

#creates three arrays: x coorddinates, y coordinates, and the values at x,y
def createArrays(val_pairs):

    x = []
    y = []
    v = []

    X_COORD = 0
    Y_COORD = 1
    VAL = 2

    for i in range(len(val_pairs)):
        x.append(val_pairs[X_COORD])
        y.append(val_pairs[Y_COORD])
        v.append(val_pairs[VAL])

    return (x,y,v)

#converys a regular python list to a numpy nd array
def convertArrayToNDArray(arr):
    return numpy.ndarray((len(arr),),dtype= float, buffer=numpy.array(arr))

#creates a scale based on the given increments and an ndarray
#returns a python list of scale values
def createScale(arr, inc):
    
    min_ = arr.min()
    max_ = arr.max()
    lis = []

    for i in range(int(min_), 100, int(max_)) :
        lis.append(i)

    return lis


pairs = processFileAsHamText(getFile())

x,y,vals = createArrays(pairs)
x = convertArrayToNDArray(x)
y = convertArrayToNDArray(y)
vals = convertArrayToNDArray(vals)

#x_scale = createScale(x)
#y_scale = createScale(y)
#val_scale = createScale(vals)




