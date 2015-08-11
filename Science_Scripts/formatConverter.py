FORMATS = ["Hamstermap Format", "Microsoft Excel Format", "Default Basic format"]
EXIT = 99

#Format Menu
def printMenu():
    print("**************Formats:****************")
    for i in range(len(FORMATS)):
        print(str(i) + " - " + FORMATS[i])

#gets valid format
def getValidFormat():
    
    isValid = False
    while(isValid != True):
        printMenu()
        ans = promptFormat()
        isValid = (type(ans) == int)

        if(isValid == True):
            return ans

#Prompts for format
def promptFormat():
    return input("Enter the format you would like to convert the data to")
    

def format(ans,coords,other):
    if(ans == 0):#ham format

        return coordsToHamstermapFormat(coords, other)

    if(ans == 1):#excel format
        return 

    if(ans == 2): #default basic format
        coordsToBasic(coords,other)
    return


#converts coordinates to hamstermap format
def coordsToHamstermapFormat(coords,other):

    string_list = []
    LAT = 0
    LONG = 1
    CO2 = 2

    default_leg = input("Use default HAM_LEGEND for legend and default Number for Number? ")


    if(default_leg == "y"): #using default legend
        for i in range(len(coords)):
            string_list.append(str(coords[i][LAT])+str("\t")+ str(coords[i][LONG]) + str("\t") +str(HAM_MARKER) + str("\t") + str(HAM_COLOR) + str("\t") + str(i+1) + str("\t") + str(HAM_LEGEND)+ str("\n"))
    else: #use custom legend
        leg = input("Enter legend to use: ")
        for i in range(len(coords)):
            string_list.append(str(coords[i][LAT])+str("\t")+ str(coords[i][LONG]) + str("\t") +str(HAM_MARKER) + str("\t") + str(HAM_COLOR) + str("\t") + str(other[i]) + str("\t") + str(leg)+ str("\n"))

    return string_list


def coordsToBasic(coords,other):

    string_list = []
    LAT = 0
    LONG = 1
    CO2 = 2

    string_list.append("Latitude\tLongitude\tCO2")
    for i in range(len(coords)):
        string_list.append(str(coords[i][LAT])+str("\t")+ str(coords[i][LONG]) + str("\t") + str(other[i]) + str("\n"))

    return string_list
