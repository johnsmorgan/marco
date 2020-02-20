# MARCO

Addendum 2020-02-20: This is a crossmatched catalogue I made around 5 years ago (pre-GLEAM, pre-TGSSADR-1) for GLEAM verification and ionospheric measurements. I have recently resurrected it to provide a rough MWA sky model for areas of the sky not currently covered by GLEAM. Please note, however, that this code made available here has not actually been run for over 5 years, so some modification may be required to get it working with current libraries.

The use of MARCO to provide a sky model for calibration of MWA data has proven to be successful. Please see the `gleam_sky_model` directory or contact me for further details. 

## Catalogues

Marco combines the following publically-available radio catalogues by making extensive use of [jystilts](http://www.star.bris.ac.uk/~mbt/stilts/sun256/jystilts.html).

[NVSS](http://vizier.u-strasbg.fr/cgi-bin/VizieR-3?-source=VIII/65)
[SUMSS](http://vizier.u-strasbg.fr/cgi-bin/VizieR-3?-source=VIII/81A)
[MGPS](http://vizier.u-strasbg.fr/cgi-bin/VizieR-3?-source=VIII/82)
[VLSS](http://www.cv.nrao.edu/vlss/CATALOG/)
[MRC](http://vizier.u-strasbg.fr/cgi-bin/VizieR-3?-source=VIII/16)
[WISH](http://vizier.u-strasbg.fr/cgi-bin/VizieR-3?-source=VIII/69A)
[WENSS](http://vizier.u-strasbg.fr/cgi-bin/VizieR-3?-source=VIII/62)
[Culgoora](http://vizier.u-strasbg.fr/cgi-bin/VizieR-3?-source=VIII/35)

These are use in the following areas:

* WENSS North of +28

* VLSS North of -30

* NVSS North of -40

* MRC South of Equator

* SUMSS South of -30

* WISH most high galactic latitudes between DEC-9 and DEC-27

## Standardising
First a "standard" version of each catalogue is produced. This is done using the script `make_standard_tables.jy`

* Units are standardised

* Flux densities are *integrated* flux densities

* Major & Minor axes and Position Angle report the source morphology *convolved with the synthesised beam of the instrument*. For the catalogues that do not report morphology, just the synthesised beam is given, as best inferred from the relevant catalogue description paper.

* All catalogue entries are given an identifier. Most catalogues have these (SUMSS does not). For those catalogues without a source ID, one is generated comforming to IAU standards.

* Errors on all quantities not provided in the original catalogue are derived from the source signal to noise.

* Flux Errors (from which many of the other errors are derived for most of the catalogues) have been truncated at about 1/30th relative of the flux. NVSS, SUMSS and MGPS have a maximum SNR of around 30.5,  (MRC even has zero errors for some of its brightest sources!!

## Crossmatching
This is done using make_marco.jy.

NVSS (north of DEC-40) and SUMSS+MGPS (south of DEC-40) are taken to be the *primary catalogues*. Each primary source is matched against all of the other catalogues in turn, generating a list of sources with between 2 and 5 flux density and morphology measurements.

The positional matching is done based on the ellipse defined by the major & minor axes and position angles of the sources in each catalogue. For each match a "Separation" value is given. This value is zero for two sources with precisely the same position, 1 when one position lies precisely on the edge of the others ellipse, and 2 where the ellipses are just touching.

## Other information
Each source in the primary catalogues is also tested to see whether there is another source within 5 arcminutes. Those which do not have a source in that region (~50%) are marked as "isolated"

The spectra have also been fitted (with a second fit for sources with more than 3 spectral points)  to give a flux and spectral index (and curvature) with errors at 150MHz. See `fit_marco.py`

## Known Issues
VLSS: The PA values run from -2631 to 2479! e_PA from 2 to 88000! These have been left as they are

Of the original catalogues which have given source ids, many have duplicates throughout the catalogue. No attempt has been made to remedy this, though the primary sources ID in the final catalogue does *not* contain any duplicates.

## Useful Filters
Choose 150MHz flux fitted with curvature where possible.

`NULL_S_150_2?S_150_1:S_150_2`

Get rid of a lot of sources right only just visible with the MwA
`DEJ2000 < 30`

Produce a more even distribution of sources.
`secondary != "wsrt" && secondary != "sumss_north"`

Given the brightness of the sources, a separation of > 0.3 is a very clear indication that the sources in the catalogues do not match perfectly. It could be an entirely spurious match, or it could be a change in the brightness distribution of the source (e.g. core dominates at higher frequency, lobes dominate at lower frequency.

`!(Separation_vlss > 0.3 || Separation_mwacs > 0.3 || Separation_mrc > 0.3 || Separation_sumss_north > 0.3 || Separation_wsrt > 0.3 || Separation_culgoora160 > 0.3 || Separation_culgoora80 > 0.3)`

Some sources are clearly very poorly matched

`SpIndex > -2.5 && SpIndex < 2.5`

`S_150 > 1`

Applying all of the above filters gives around 1 per 3 square degrees > 1Jy with a fairly even distribution.

## Suggestions for future work
The main weakness of this catalogue is that it makes no attempt to match multiple sources at the higher-resolution end to a single source at lower resolution.

The low-hanging fruit here would be to combine the ~100000 close doubles (separation <1 arcmin) in the original catalogues before crossmatching. New combined sources could be made by summing the flux densities and producing new source parameters from the separation of the two sources and the dot product of the original major/minor axes with the difference between the original and new position angle.

This would still leave a significant triple and larger groups. At some level working out sensible groupings of sources becomes an issue.
