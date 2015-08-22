;--load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

;--retrieves file names
function get_file_names()
local names,tmp_str
begin
	tmp_str = systemfunc("find /home/Bama4/OCO2_DATA/ -name '*.h5' >> file_names.txt")
	;--print(tmp_str)
	names = asciiread("file_names.txt",-1,"string")
	return names
end


;--gets data from all files in the given directory
function processFiles(names)
local longs,lats,data,counter,file_tmps,files_0,tmp 

begin

	files_0 = addfile(names(0),"r")
	counter = 0

	;--set arrays for longitude and latitude
	longs = new(1,float)
	lats = new(1,float)
	data = new(1,float)
	tmp = new(1,float)

	copy_VarMeta(files_0->retrieval_longitude, longs)
	copy_VarMeta(files_0->retrieval_latitude, lats)
	copy_VarMeta(files_0->xco2, data)
	
	
	print("Opening files")
	print(dimsizes(names))

;--get data from all files found
do while (counter .lt. dimsizes(names))
	
	delete(files_0)
	files_0 = addfile(names(counter),"r")
	print(counter)
	print(longs)
	
	longs = array_append_record(files_0->retrieval_longitude,longs,0)
	data = array_append_record(files_0->xco2,data,0)
	lats = array_append_record(files_0->retrieval_latitude,lats,0)
	counter = counter + 1
end do
	return ([/longs,lats,data/])
end

function get_data_()
local n,tmp_list
begin
	n = get_file_names()
	tmp_list = processFiles(n)
	print(tmp_list)
	return tmp_list
end
