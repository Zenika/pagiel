# Maintainers

## New release

Update the following variables of the [.env-default](.env-default) with the value of the tag to be released (the images will be built upon the creation of the tag and tagged with it's name):
 - SITESPEED_IMAGE_VERSION=zenika/pagiel-sitespeed:\<tag>
 - GREENIT_ANALYSIS_IMAGE_VERSION=zenika/pagiel-greenit-analysis-cli:\<tag>
 - YELLOWLABTOOLS_IMAGE_VERSION=zenika/pagiel-yellowlabtools:\<tag>
 - URL_CONVERTER_IMAGE_VERSION=zenika/pagiel-url-converter:\<tag>
 - REPORT_IMAGE_VERSION=zenika/pagiel-report:\<tag>
 - ROBOT_IMAGE_VERSION=zenika/pagiel-robot-framework:\<tag>

 To trigger the pipeline, the tag must have the form `X.X.X` . It will automaticaly build the images and upload them in the docker repository. The images will have the same tag as the tag created in gitlab.
