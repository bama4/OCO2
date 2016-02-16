import mysql.connector as SQL
import OCO2_Driver as Handle



class SQL_Driver:
    
    def __init__(self,schema,pwd):
        self.cnx = SQL.connect(user='root', database= schema, password=pwd)
        self.cursor = self.cnx.cursor()
        self.curr_table = ""
        
    def updateCurrTable(self,new_table):
        self.curr_table = new_table
    # 
    # def getCNXData():
    #     dat = []
    #     
    #     for 
        
    def getSiteData(self, s_name,s_lon,s_lat,s_data,s_year, s_month, s_day,name):
        
        query = ("SELECT {0} , {1}, {2} , {3}, {4}, {5}, {6} FROM {7} WHERE {0} = \"{8}\" ORDER BY {4},{5},{6}".format(
        
            s_name,
            s_lon,
            s_lat,
            s_data,
            s_year, 
            s_month, 
            s_day,
            self.curr_table,
            name
            
            )
        )
            
        print(query)
        self.cursor.execute(query)
            
    def getSiteDataByMonth(self, s_name,s_lon,s_lat,s_data,s_year, s_month, s_day,name,year,month):
        
        
        query = ("SELECT {0} , {1}, {2} , {3}, {4}, {5}, {6} FROM {7} WHERE {0} = \"{8}\" AND {5} = {9} ORDER BY {4},{5},{6}".format(
        
            s_name,
            s_lon,
            s_lat,
            s_data,
            s_year, 
            s_month, 
            s_day,
            self.curr_table,
            name,
            month
            )
        )
            
        print(query)
        self.cursor.execute(query)
        
    #Retrieves given name year month and day data from corresponding named columns s_name, s_year etc. 
    #range is a tuple in which ([yyyy,mm,dd],[yyyy,mm,dd])
    def getDataDateRange(self, s_name,s_data,s_year, s_month, s_day,name, range):
        YEAR = 0
        MONTH = 1
        DAY = 2
        query = ("SELECT {0} , {1}, {2} , {3}, {4} FROM {5} WHERE {2} BETWEEN {6} AND {7} AND {3} BETWEEN {8} AND {9} AND {4} BETWEEN {10} AND {11}".format(
        
            s_name,
            s_data,
            s_year, 
            s_month, 
            s_day,
            self.curr_table,
            range[0][YEAR], 
            range[1][YEAR],
            range[0][MONTH], 
            range[1][MONTH],
            range[0][DAY], 
            range[1][DAY],
            ) 
        )
        print(query)
        self.cursor.execute(query)
        
    
    #Retrieves given name long.lat , year month and day data from corresponding named columns s_name, s_year etc. 
    #range is a tuple in which ((lat,long)(lat,long))
    def getDataCoordRange(self, s_name,s_long,s_lat,s_data,s_year, s_month, s_day,name, range):
        LAT = 0
        LON = 1
        
        query = ("SELECT {0} , {1}, {2} , {3}, {4}, {5} , {6} FROM {7} WHERE {1} BETWEEN {8} AND {10} AND {2} BETWEEN {9} AND {11}".format(
        
            s_name, # 0
            s_long, # 1
            s_lat,  # 2
            s_data, # 3
            s_year, # 4
            s_month,# 5
            s_day,  # 6
            self.curr_table, # 7
            range[0][LONG],  # 8
            range[1][LAT],  # 9
            range[0][LONG], # 10
            range[1][LAT] # 11

            ) 
        )
        
        print(query)
        self.cursor.execute(query)
    
    def getDataDateAndCoordRange(self, s_name,s_long,s_lat,s_data,s_year, s_month, s_day,name, range_coord, range_date):
    
        YEAR = 0
        MONTH = 1
        DAY = 2
        
        LAT = 0
        LONG = 1
        
        query = ("SELECT {0} , {1}, {2} , {3}, {4}, {5} , {6} FROM {7} WHERE {1} BETWEEN {8} AND {10} AND {2} BETWEEN {9} AND {11} AND {4} BETWEEN {12} AND {13} AND {5} BETWEEN {14} AND {15} AND {6} BETWEEN {16} AND {17} AND Name = {0}".format(
        
            s_name, # 0
            s_long, # 1
            s_lat,  # 2
            s_data, # 3
            s_year, # 4
            s_month,# 5
            s_day,  # 6
            self.curr_table, # 7
            range_coord[0][LONG],  # 8
            range_coord[0][LAT],  # 9
            range_coord[1][LONG], # 10
            range_coord[1][LAT], # 11
            range_date[0][YEAR], # 12
            range_date[1][YEAR], # 13
            range_date[0][MONTH],# 14
            range_date[1][MONTH],# 15
            range_date[0][DAY],  # 16
            range_date[1][DAY]   # 17
            ) 
        )
        
        print(query)
        self.cursor.execute(query)
    
    
    def convertDataToMPlot(record):
        pass
        
        
  