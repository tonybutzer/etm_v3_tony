import sys

jobname='conus_mos_netet_'

yr1 = '2003'
yr2 = '2004'


def out_bat_file(yr1):
	my_here = f'''#!/bin/sh

#SBATCH --account=impd
#SBATCH --time=36:00:00
#SBATCH --job-name={yr1}_netet
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
python3 conus_api_etm.py  -y {yr1} --in /caldera/projects/usgs/water/impd/skagone --out /caldera/projects/usgs/water/impd/skagone/conus_mos_completed/{yr1} netet


'''

	print('This message will be displayed on the screen.')

	original_stdout = sys.stdout # Save a reference to the original standard output

	with open(f'3_netet_batch/gen_batch_{yr1}.sh', 'w') as f:
	    sys.stdout = f # Change the standard output to the file we created.
	    print(my_here)
	    sys.stdout = original_stdout # Reset the standard output to its original value
	print(my_here)

for yr1 in range(1984, 2021):
	print(yr1)
	out_bat_file(yr1)
  
