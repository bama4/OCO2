import math


DEFAULT_FILE = 'C:/Users/Bama4/Documents/nsa30ecorE10.b1.20150803.000000.custom.cdf'

#format to hamster map
def formatToHamMap():
    pass

#returns file contents
def getFileContents(file_name):

    try:

        nc = NetCDFFile(file_name)
        file_contents = []

        for line in f:
            file_contents.append(line.strip().split(""))
        return file_contents

    except StandardError:
        print("Invalid")
        return

#prompt with the following given 'msg'
def promptPrint(msg):
    return input(msg)


def main():

    ans = promptPrint("Enter the name of the file")
    
    if (ans == "DEFAULT_FILE"):
        getFileContents(DEFAULT_FILE)
    else:
        getFileContents(ans)
main()
