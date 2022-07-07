#!/bin/sh

#SBATCH --account=impd
#SBATCH --time=36:00:00
#SBATCH --job-name=1984_netet
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

for yr in {1985..1989}; do {

	python3 conus_api_etm.py  -y ${yr} --in /caldera/projects/usgs/water/impd/skagone/1_MONTHLY_ONLY/etasw --out /caldera/projects/usgs/water/impd/skagone/2_MONTHLY_MOSAICS/${yr} etasw


}; done


