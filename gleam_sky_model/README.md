## Complementing GLEAM-X sky model with MARCO

Included in this directory is `gaps.fits`. These sources in this catalogue cover complementary parts of the sky to those covered by the [GLEAM-X pipeline model](https://github.com/nhurleywalker/GLEAM-X-pipeline/blob/master/models/skymodel_only_alpha.fits)
These two catalogues can be combined using `fill_in_gleam_skymodel.sh`.

## Generating the sky model from MARCO
This assumes that you have successfully run all of the scripts in the parent directory.
Producing `gaps.fits` is done with the following scripts in this order:
`make_gleam_skymodel.sh`
`concat_gaps.sh`
