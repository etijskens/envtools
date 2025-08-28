#!/bin/bash
#SBATCH --job-name envtools
#SBATCH --output=slurm-%x.%j.out
#SBATCH --time=0:05:00
#SBATCH --mem=0
#SBATCH --account=project_465000095
#SBATCH --nodes=1 --tasks-per-node=4 --cpus-per-task=1
#SBATCH --partition=small

. /pfs/lustrep4/projappl/project_465000095/entijske/tantalus_full/experiments/env/ml.sh

python /pfs/lustrep4/projappl/project_465000095/entijske/envtools/envtools/__init__.py