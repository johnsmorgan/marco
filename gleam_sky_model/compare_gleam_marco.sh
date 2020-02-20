stilts tpipe \
	in=skymodel_only_alpha.fits \
	cmd='select RAJ2000<30&&DEJ2000>0&&DEJ2000<30' \
	out=skymodel_control.fits

stilts tmatch2 \
	in1=control.fits \
	in2=skymodel_control.fits \
	matcher=sky \
	values1="RAJ2000 DEJ2000" \
	values2="RAJ2000 DEJ2000" \
	params=60 \
	out=control_xmatch.fits

topcat -stilts plot2plane \
   xpix=512 \
   xlog=true ylog=true xlabel=S_200 \
    ylabel= \
   xmin=0 xmax=51.2 ymin=1 \
    ymax=1207 \
   legend=true \
   x=S_200 \
   title="Counts in overlap region" \
   layer_1=Histogram \
      in_1=/data/catalogs/marco/gleam_sky_model/control.fits \
      leglabel_1=MARCO \
   layer_2=Histogram \
      in_2=/data/catalogs/marco/gleam_sky_model/skymodel_control.fits \
      color_2=blue \
      leglabel_2=GLEAM \
   omode=out out=gleam_marco_counts.png

topcat -stilts plot2plane \
   xpix=512 ypix=512\
   xlog=true ylog=true xlabel=MARCO ylabel=GLEAM \
   xmin=0.1 xmax=32.9 ymin=0 ymax=44.6 \
   legend=false \
   title="Flux density comparison of matching sources" \
   layer_1=Mark \
      in_1=/data/catalogs/marco/gleam_sky_model/control_xmatch.fits \
      x_1=S_200_1 y_1=S_200_2 \
      shading_1=auto \
   layer_2=Function \
      fexpr_2='x' color_2=grey \
      leglabel_2='x'  \
   omode=out out=gleam_marco_s200.png

topcat -stilts plot2plane \
   xpix=512 ypix=512 \
   xlabel=MARCO ylabel=GLEAM \
   xmin=-2 xmax=2 ymin=-2 ymax=2 \
   legend=false \
   title="Spectral index comparison of matching sources" \
   layer_1=Mark \
      in_1=/data/catalogs/marco/gleam_sky_model/control_xmatch.fits \
      x_1=alpha_1 y_1=alpha_2 \
      shading_1=auto \
   layer_2=Function \
      fexpr_2='x' color_2=grey \
      leglabel_2='x'  \
   omode=out out=gleam_marco_alpha.png

topcat -stilts plot2sky \
   xpix=934 ypix=586 \
   projection=aitoff \
   legend=true \
   lon=RAJ2000 lat=DEJ2000 shading=auto \
   layer_1=Mark \
      in_1=/data/catalogs/marco/gleam_sky_model/skymodel_only_alpha.fits \
      leglabel_1='GLEAM-derived sky model' \
   layer_2=Mark \
      in_2=/data/catalogs/marco/gleam_sky_model/gaps_unique.fits \
      color_2=blue \
      leglabel_2='Filled in with other surveys' \
   omode=out out=gleam_marco_coverage.png
