import matplotlib as mat
import matplotlib.pyplot as plt
import numpy as np
import os
import math 
import MySQL_Driver
import OCO2_Driver

S_DRIVER = MySQL_Driver.SQL_Driver("sciencedata","123")
COMMANDS = ["Set Data of Region as Current DataSet", "Grid Data by region", "Grid Data by region, year, month","Plot monthly Data By Region", "Display current data","Plot monthly Data and Compare By Region"]

EXIT = 99

#display the menu
def displayMenu():
    
    for i in range(len(COMMANDS)):
        print(str(i) + " - " + COMMANDS[i])

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

        

def gridData(res): #gives data located in S_DRIVER.cursor for gridding
    
    np_arrays = []
    
    g_longs = []
    g_lats = []
    g_time = []
    g_data = []
    
    name = ""
    longs = [] # 1
    lats = []  # 2
    data = [] # 3
    time_doy = [] # 4 , 5 , 6
    time_ = []    # 4 , 5 , 6
    
    for entry in S_DRIVER.cursor:
        name = entry[0]
        time_tmp = [entry[4],entry[5],entry[6]]
        time_doy.append(OCO2_Driver.dateToDOY(time_tmp))
        time_.append(time_tmp)
        data.append(entry[3])
        longs.append(entry[1])
        lats.append(entry[2])
    
    
    
    return (name, longs, lats , data, time_doy,time_)


#data in format (name, longs, lats , data, time_doy,time_)
def avgMonthly(data,year):
    
    data_m_avg = 0
    num_days_in_curr_month = 0
    month_data_avg = []
    month_ = []
    curr_month = 0
    num_months = 0
    
    for i in range(len(data[5])):
        
        
        if(data[5][i][0] != year):
            continue
            
        if(curr_month == 0):
            
            curr_month = data[5][i][1]
            
        elif(curr_month != data[5][i][1]):

            data_m_avg = data_m_avg/(num_days_in_curr_month*1.0)
            month_data_avg.append(data_m_avg)
            month_.append(curr_month)
            num_days_in_curr_month = 0
            data_m_avg = 0
            
            curr_month = data[5][i][1]
            num_months += 1
        
            
        num_days_in_curr_month += 1
        data_m_avg += data[3][i]
    return month_data_avg , month_
    
    
#data in format (name, longs, lats , data, time_doy,time_)
def plotByMonth(data,year):
    
    
    month_data_avg,month_ = avgMonthly(data,year)
    print(month_data_avg)
    print(month_)

    title = data[0] + " "  + str(year)
    plt.figure().suptitle(title)
    plt.ylabel("CO2 in PPM")
    plt.xlabel("MONTHS")
    plt.plot( np.array(month_), np.array(month_data_avg),'ro')
    plt.axis([ 1 , 12,300 , 600 ])
    plt.yticks(np.arange(300,600,10))
    plt.xticks(np.arange(1,12,1))
    plt.show()
        
            
def plotByMonth2(data1,data2,year):

    title = data1[0] + " VS " + data2[0] + str(year)

    month_data_avg1,month1_ = avgMonthly(data1,year)
    month_data_avg2,month2_ = avgMonthly(data2,year)
    
    print(month_data_avg1)
    print(month1_)

    print(month_data_avg2)
    print(month2_)
    
    plt.figure().suptitle(title)
    plt.ylabel("CO2 in PPM")
    plt.xlabel("MONTHS")
    plt.plot( np.array(month1_), np.array(month_data_avg1),'bo',np.array(month2_), np.array(month_data_avg2),'ro')
    plt.axis([ 1 , 12,380 , 450 ])
    plt.yticks(np.arange(380,450,2.0))
    plt.xticks(np.arange(1,12,1))
    plt.show()


#taken from  https://scipy.github.io/old-wiki/pages/Cookbook/Matplotlib/Gridding_irregularly_spaced_data.html
def griddata(x, y, z, binsize=0.01, retbin=True, retloc=True):

# get extrema values.
    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()
 
     # make coordinate arrays.
    xi      = np.arange(xmin, xmax+binsize, binsize)
    yi      = np.arange(ymin, ymax+binsize, binsize)
    xi, yi = np.meshgrid(xi,yi)
  
     # make the grid.
    grid           = np.zeros(xi.shape, dtype=x.dtype)
    nrow, ncol = grid.shape
    if retbin: bins = np.copy(grid)
      
     # create list in same shape as grid to store indices
    if retloc:
        wherebin = np.copy(grid)
        wherebin = wherebin.tolist()
  
    # fill in the grid.
    for row in range(nrow):
        for col in range(ncol):
            xc = xi[row, col]    # x coordinate.
            yc = yi[row, col]    # y coordinate.
 
              # find the position that xc and yc correspond to.
            posx = np.abs(x - xc)
            posy = np.abs(y - yc)
            ibin = np.logical_and(posx < binsize/2., posy < binsize/2.)
            ind  = np.where(ibin == True)[0]
        
            # fill the bin.
            bin = z[ibin]
            if retloc: wherebin[row][col] = ind
            if retbin: bins[row, col] = bin.size
            if bin.size != 0:
                binval         = np.median(bin)
                grid[row, col] = binval
            else:
                grid[row, col] = np.nan   # fill empty bins with nans.
 
    # return the grid
    if retbin:
        if retloc:
            return grid, bins, wherebin
        else:
            return grid, bins
    else:
        if retloc:
            return grid, wherebin
        else:
            return grid
#taken from  https://scipy.github.io/old-wiki/pages/Cookbook/Matplotlib/Gridding_irregularly_spaced_data.html
def showContour(data):
    title = data[0]
    lon = data[1]
    lat = data[2]
    data_ = data[3]
    time_ = data[4]

    npr = np.random
    npts = len(data_)                            # the total number of data points.
    x = lon            # create some normally distributed dependent data in x.
    y = lat            # ... do the same for y.
    z = data_
  
  # plot some profiles / cross-sections for some visualization.  our
  # function is a symmetric, upward opening paraboloid z = x**2 + y**2.
  # We expect it to be symmetric about and and y, attain a minimum on
  # the origin and display minor Gaussian noise.
  
    plt.ion()   # pyplot interactive mode on
  
  # x vs z cross-section.  notice the noise.
    plt.plot(x, z, '.')
    plt.title('X vs Z=F(X,Y)' + title)
    plt.xlabel('X')
    plt.ylabel('Z')

  # y vs z cross-section.  notice the noise.
    plt.plot(y, z, '.')
    plt.title('Y vs Z=F(Y,X=constant)')
    plt.xlabel('Y')
    plt.ylabel('Z')
  
  # now show the dependent data (x vs y).  we could represent the z data
  # as a third axis by either a 3d plot or contour plot, but we need to
    # grid it first....
    plt.plot(x, y, '.')
    plt.title('X vs Y')
    plt.xlabel('X')
    plt.ylabel('Y')
    
    # enter the gridding.  imagine drawing a symmetrical grid over the
   # plot above.  the binsize is the width and height of one of the grid
    # cells, or bins in units of x and y.
    binsize = 0.3
    grid, bins, binloc = griddata(x, y, z, binsize=binsize)  # see this routine's docstring
  
  
    # minimum values for colorbar. filter our nans which are in the grid
    zmin    = grid[np.where(np.isnan(grid) == False)].min()
    zmax    = grid[np.where(np.isnan(grid) == False)].max()
  
    # colorbar stuff
    palette = plt.matplotlib.colors.LinearSegmentedColormap('jet3',plt.cm.datad['jet'],2048)
    palette.set_under(alpha=0.0)
  
    # plot the results.  first plot is x, y vs z, where z is a filled level plot.
    extent = (x.min(), x.max(), y.min(), y.max()) # extent of the plot
    plt.subplot(1, 2, 1)
    plt.imshow(grid, extent=extent, cmap=palette, origin='lower', vmin=zmin, vmax=zmax, aspect='auto', interpolation='bilinear')
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.title('Z = F(X, Y)')
    plt.colorbar()
    
def procCommands(c):
    
    
   
        
    if c == 0: #set data of region as current dataset
        
        nam = input("Enter region name")
        
        S_DRIVER.getSiteData("Name","Longitude","Latitude","DATA_VAL", "YEAR", "MONTH", "DAY", nam)
        return
    
    if c == 1: #grid data by region
    
       
        
        data = gridData()
        showContour(data)
        
        return
    
    if c == 2: #grid data by region, year, month
        data = gridData()
        showContour(data)
        return 
        
    if c == 3:#make plot of time vs. month
        
        year = int(input("Enter year"))
        data = gridData(0)
        plotByMonth(data,year)
        return
        
    if c == 4:
        
        for i in S_DRIVER.cursor:
            print(i)
        return
        
    if c == 5:
        
        nam = input("Enter 1st region name")
        
        S_DRIVER.getSiteData("Name","Longitude","Latitude","DATA_VAL", "YEAR", "MONTH", "DAY", nam)
        year = int(input("Enter year"))
        data1 = gridData(0)
        
        
        nam = input("Enter 2nd region name")
        
        S_DRIVER.getSiteData("Name","Longitude","Latitude","DATA_VAL", "YEAR", "MONTH", "DAY", nam)
        data2 = gridData(0)
        
        
        plotByMonth2(data1,data2,year)
    
        return
        
    if c == EXIT:
        print("BYE")
        sys.exit(0)
        return
            

def main():
    
    
    S_DRIVER.updateCurrTable("sites")
    
    while(True):
        
        inp = getInput()
        procCommands(inp)
        print("\n\n\n")
        
    print(inp)
main()