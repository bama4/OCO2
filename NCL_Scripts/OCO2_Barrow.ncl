load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "/home/Bama4/OCO2_Data/OCO2_Script_LITE.ncl"

begin

	;-- Bounds for Region
	lon0 = -153.0
	lon1 = -163.0
	lat0 = 72.4
	lat1 = 69.0

	;-- Region coordinates and data
	
	list_tmp = get_data_()
	
	longitudes = list_tmp[0]
	latitudes = list_tmp[1]
	var = list_tmp[2]

	;-- define the workstation (plot type and name)
	wks = gsn_open_wks("png","unstructured_grid")

	var@_FillValue = -1
	;-- set resources
	res = True
	res@gsnMaximize = True ;-- maximize plot output
	res@cnFillOn = True ;-- turn on contour fill
	res@cnFillPalette = "rainbow"  
	res@cnLinesOn            = False              
	res@tiMainString = "World Map"
	res@tiMainFontHeightF = 0.02
	res@cnFillMode = "RasterFill"
	res@cnRasterSmoothingOn = True
	res@sfXArray = list_tmp[0]
	res@sfYArray = list_tmp[1]

	;--res@mpMinLatF = lat1
	;--res@mpMaxLatF = lat0
	;--res@mpMinLonF = lon1
	;--res@mpMaxLonF = lon0
	;--res@gsnSpreadColors      = True
	;--manually set the contour levels with the following 3 resources
	
	 resP                     = True   
  	resP@gsnMaximize         = True 
        res@cnLevelSelectionMode = "ManualLevels"	
        res@cnMinLevelValF  = 375.0
        res@cnMaxLevelValF  = 425.0			
  	res@cnLevelSpacingF = 0.5	
	
	;--opt = True
  	;--opt@PrintStat = True
  	;--statb = stat_dispersion(var, opt )
        ;--printVarSummary(var)
        ;--printMinMax(var,0)
	;--draw the contour map
	plot = gsn_csm_contour_map(wks, var, res)
	
end

