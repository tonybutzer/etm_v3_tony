#! /bin/bash

for yr in 1986 1987; do echo $yr; sbatch 2_batch/gen_batch_${yr}.sh; done
