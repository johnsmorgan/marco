#NB old code for fitting SEDs in MARCO is > 5 years old and needs rewriting to work with modern library version
# since it's only a fairly modest change in frequency, should be ok to use S_150 and alpha to calculate S_200
stilts tpipe \
	in=../marco_150_alpha_fixed.fits \
        cmd='keepcols "ID RAJ2000 DEJ2000 S_150_1 SpIndex_1 MajAxis MinAxis PA primary secondary"' \
	cmd='colmeta -name Name ID' \
	cmd='colmeta -name alpha SpIndex_1' \
	cmd='colmeta -name a MajAxis' \
	cmd='colmeta -name b MinAxis' \
	cmd='addcol -after alpha beta toDouble(0.0)' \
	cmd='replacecol S_150_1 S_150_1*pow(200.0/150.0,alpha)' \
	cmd='replacecol alpha toDouble(alpha)' \
	cmd='colmeta -name S_200 S_150_1' \
	cmd='select S_200>0.1' \
	cmd='select secondary!=\"wsrt\"&&secondary!=\"sumss_north\"' \
	out=marco_200.fits

stilts tpipe \
	in=marco_200.fits \
	cmd='select RAJ2000>330&&DEJ2000>0&&DEJ2000<30' \
	out=gap1.fits

# control region, for comparing GLEAM and MARCO
stilts tpipe \
	in=marco_200.fits \
	cmd='select RAJ2000<30&&DEJ2000>0&&DEJ2000<30' \
	out=control.fits

stilts tpipe \
	in=marco_200.fits \
	cmd='select RAJ2000>195&&RAJ2000<210&&DEJ2000>20&&DEJ2000<30' \
	out=gap2.fits

stilts tpipe \
	in=marco_200.fits \
	cmd='select DEJ2000>30' \
	out=north.fits
