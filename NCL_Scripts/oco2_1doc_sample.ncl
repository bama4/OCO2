load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "/home/Bama4/OCO2_Data/OCO2_Script.ncl"

begin

	PATH = "C:\cygwin\home\Bama4\OCO2_DATA\July_Test_Week\186\oco2_L2StdND_05366a_150705_B7000_150707113934.h5"
	;-- Bounds for Region
	lon0 = -153.0
	lon1 = -163.0
	lat0 = 72.4
	lat1 = 69.0

	;-- Region coordinates and data
	
	list_tmp = addfile(PATH,"r")
	
	longitudes = list_tmp->retrieval_longitude
	latitudes = list_tmp->retrieval_latitude
	var = list_tmp->xco2

	avg_data = avg(var)
	var = abs(avg_data-var)*SCALE

	;-- define the workstation (plot type and name)
	wks = gsn_open_wks("png","unstructured_grid")
	
	;-- set resources
	res = True
	res@gsnMaximize = True ;-- maximize plot output
	res@cnFillOn = True ;-- turn on contour fill
	res@cnFillPalette = "rainbow" ;-- choose a colormap
	res@tiMainString = "World Map July Sample"
	res@tiMainFontHeightF = 0.02
	
	
	res@sfXArray = list_tmp->retrieval_longitude
	res@sfYArray = list_tmp->retrieval_latitude

	;--res@mpMinLatF = lat1
	;--res@mpMaxLatF = lat0
	;--res@mpMinLonF = lon1
	;--res@mpMaxLonF = lon0

	;-- draw the contour map
	plot = gsn_csm_contour_map(wks, var, res)

	
end

