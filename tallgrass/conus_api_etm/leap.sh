#! /bin/bash

for yr in 2004 2008 2012 2016 2020; do {
	echo $yr
	python3 conus_api_etm.py  -y $yr --in /caldera/projects/usgs/water/impd/skagone --out /caldera/projects/usgs/water/impd/skagone/conus_mos_completed/$yr netet
}; done
