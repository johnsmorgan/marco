# concatenate gaps in sky model
stilts tcat in=gap1.fits in=gap2.fits in=north.fits out=gaps.fits

# remove anything which already has a match in the current sky model
stilts tmatch2 \
	in1=gaps.fits \
	in2=skymodel_only_alpha.fits \
	icmd1='delcols "primary secondary"' \
	matcher=sky find=best1 join=1not2 \
	values1="RAJ2000 DEJ2000" \
	values2="RAJ2000 DEJ2000" \
	params=60 \
	out=gaps_unique.fits

# concatenate gaps and GLEAM-based sky model
stilts tcat in=skymodel_only_alpha.fits in=gaps_unique.fits \
	ocmd="sort name" \
	out=skymodel_allsky_only_alpha.fits
