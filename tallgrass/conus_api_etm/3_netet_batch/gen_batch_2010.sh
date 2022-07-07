#!/bin/sh

#SBATCH --account=impd
#SBATCH --time=36:00:00
#SBATCH --job-name=2010_netet
#SBATCH -o %j_log.out
#SBATCH --error=%j_err.err
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH --mail-type=ALL
#SBATCH --mail-user=skagone@contractor.usgs.gov

# load analytics and cuda modules
source /home/skagone/miniconda3/bin/activate steffi

# run the mosaic
python3 conus_api_etm.py  -y 2010 --in /caldera/projects/usgs/water/impd/skagone --out /caldera/projects/usgs/water/impd/skagone/conus_mos_completed/2010 netet



