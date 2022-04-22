#!/bin/sh

#SBATCH --account=impd
#SBATCH --time=16:00:00
#SBATCH --job-name=conus_mos2012_netet
#SBATCH -o %j_log.out
#SBATCH --error=%j_err.err
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH --mail-type=ALL
#SBATCH --mail-user=butzer@contractor.usgs.gov

# load analytics and cuda modules
source /home/butzer/miniconda3/bin/activate pangeo

# run the mosaic
python3 conus_api_etm.py  -y 2013 --in /caldera/projects/usgs/water/impd/skagone --out /caldera/projects/usgs/water/impd/butzer/2013 netet

