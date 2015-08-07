import math

#format to hamster map
def formatToHamMap():
    pass

#returns file contents
def getFileContents(file_name):

    try:

        f = open(file_name,"r")
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

    promptPrint("Enter the name of the file")

main()
