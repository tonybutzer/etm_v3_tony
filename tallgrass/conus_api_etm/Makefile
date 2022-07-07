cat:
	cat Makefile

test:
	python3 conus_api_etm.py  -y 2014 --in /caldera/projects/usgs/water/impd/skagone --out /caldera/projects/usgs/water/impd/butzer/2014 netet


steffi:
	ls /caldera/projects/usgs/water/impd/skagone

batch:
	sbatch batch.sh

sq:
	squeue | grep skagone

run:
	python3 conus_api_etm.py  -y 2000 --in /caldera/projects/usgs/water/impd/skagone --out /caldera/projects/usgs/water/impd/skagone/conus_mos_completed/2000 etasw

jup:
	echo "ssh -N -L 8888:`hostname`:8888  `whoami`@tallgrass.cr.usgs.gov"
	jupyter lab --no-browser --ip=`hostname` --port=8888

