load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "/home/Bama4/OCO2_Data/OCO2_Script.ncl"
begin
	PATH = "/home/Bama4/OCO2_DATA/185/oco2_L2StdGL_05341a_150704_B7000_150705155753.h5"

	;-- Bounds for Region
	lon0 = -153.0
	lon1 = -163.0
	lat0 = 72.4
	lat1 = 69.0

	;-- Region coordinates and data
	
	list_tmp = get_data_()
	;--print(list_tmp)

	longitudes = list_tmp[0]
	latitudes = list_tmp[1]
	var = list_tmp[2]

	;-- define the workstation (plot type and name)
	wks = gsn_open_wks("png","unstructured_grid")
	;-- set resources
	res = True
	res@gsnMaximize = True ;-- maximize plot output
	res@cnFillOn = True ;-- turn on contour fill
	res@cnFillPalette = "rainbow" ;-- choose a colormap
	res@tiMainString = "World Map July"
	res@tiMainFontHeightF = 0.02
	
	
	res@sfXArray = longitudes
	res@sfYArray = latitudes

	;--res@mpMinLatF = lat1
	;--res@mpMaxLatF = lat0
	;--res@mpMinLonF = lon1
	;--res@mpMaxLonF = lon0

	;-- draw the contour map
	plot = gsn_csm_contour_map(wks, var, res)
	draw(plot)
end

