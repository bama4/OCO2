import matplotlib as mat

import os
import math 


#File object ( name , pathname )
class LinePlot:
    
    
    #init constructor
    def __init__(self,title,path):
        self.title = title
        self.path = path
        self.data = {}
        self.obj = None
        
    
        