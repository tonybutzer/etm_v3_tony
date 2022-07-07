#!/bin/sh

#SBATCH --account=impd
#SBATCH --time=36:00:00
#SBATCH --job-name=conus_1985_netet
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
year=1986
python3 conus_api_etm.py  -y $year --in /caldera/projects/usgs/water/impd/skagone --out /caldera/projects/usgs/water/impd/skagone/conus_mos_completed/${year} netet


