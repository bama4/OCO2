load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

DEFAULT_CONT = 0.001
SCALE = 1000000

;--adjust contour levels
;--returns contour levels based on the default scale
function adjContour(data)
local max_n,min_n

begin
max_n = max(data)
min_n = min(data)
end

;--retrieves file namess
function get_file_names()
local names,tmp_str
begin
	tmp_str = systemfunc("find /home/Bama4/OCO2_DATA/July_Test_Week/181 -name '*.h5' ") ; July 
	
	return tmp_str
end

;--gets data from all files in the given directory
function processFiles(names)
local longs,lats,data,files_0,avg_data 

begin


	files_0 = addfiles(names,"r")
	longs = files_0[:]->retrieval_longitude
  	lats  = files_0[:]->retrieval_latitude   
 	data  = files_0[:]->xco2
	avg_data = avg(data)	

	;--data = abs(data - avg_data)*SCALE 
	;--scale values
	
	data = data*SCALE

	delete(files_0)
	delete(avg_data)
	return ([/longs,lats,data/])
	
	
end

function get_data_()
local n,tmp_list
begin
	n = get_file_names()
	tmp_list = processFiles(n)
	
	return tmp_list
end

