load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "/home/Bama4/GREY_NOV_DATA.ncl"
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

  ;--map = gsn_csm_map(wks,res)               
  ; Create the map plot, don't draw

  mkres               = True
  ;--mkres@gsMarkerIndex = 2
  ;--mkres@gsMarkerColor = "Brown"

  ;--gsn_polymarker(wks,map,lon,lat,mkres)

  ;--frame(wks)

;
; Zoom in even more on the map.
;

  lon0 = -105.1019
  lon1 = -105.6019
  lat0 = 48.8077
  lat1 = 48.3077

  res@mpMaxLatF =   lat0
  res@mpMaxLonF =   lon0
  res@mpMinLatF =   lat1
  res@mpMinLonF =   lon1


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
