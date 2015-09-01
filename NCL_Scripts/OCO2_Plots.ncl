load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "/home/Bama4/OCO2_Data/OCO2_Script.ncl"
;************************************************
begin
;************************************************
; Generate some random data
;************************************************
 f = get_data_()

  lat = f[1]
  lon = f[0]
;
; There are some stations with lat/lon values outside range, so
; set these to missing.
;
  ;--lat = where(lat.lt. -90.or.lat.gt. 90,lat@_FillValue,lat)
  ;--lon = where(lon.lt.-180.or.lon.gt.180,lon@_FillValue,lon)

  wks   = gsn_open_wks ("png","scatter")               ; open workstation

  res             = True                              ; plot mods desired
  res@gsnFrame    = False                             ; don't advance yet
  res@gsnMaximize = True

  ;--res@mpMinLatF = min(lat) - 5
  ;--res@mpMaxLatF = max(lat) + 5
  ;--res@mpMinLonF = min(lon) - 5
  ;--res@mpMaxLonF = max(lon) + 5
  ;--res@tiMainString = "Locations of stations"

  map = gsn_csm_map(wks,res)                ; Create the map plot, don't draw

  mkres               = True
  mkres@gsMarkerIndex = 2
  mkres@gsMarkerColor = "Brown"

  gsn_polymarker(wks,map,lon,lat,mkres)

  frame(wks)

;
; Zoom in even more on the map.
;
  res@mpMaxLatF =   60.
  res@mpMaxLonF =  -65.
  res@mpMinLatF =   22.
  res@mpMinLonF = -125.

  map = gsn_csm_map(wks,res)                ; Create the map plot, don't draw

;
; Now attach the markers to the plot and notice that you don't
; see them until you draw the plot.
;
; If you resize the plot, the markers will be resized accordingly.
;
  mkres@gsMarkerColor = "Blue"
  mkres@gsMarkerSizeF = 15.        ; Increase marker sizes.

  dum = gsn_add_polymarker(wks,map,lon,lat,mkres)

  draw(map)
  frame(wks)

end
