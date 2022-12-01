#!/bin/bash --login
#SBATCH --job-name=moap-test
#SBATCH --time=1:00:00
#SBATCH --account=d435
#SBATCH --partition=standard
#SBATCH --qos=lowpriority
#SBATCH --nodes=1
#SBATCH --tasks-per-node=6
#SBATCH --cpus-per-task=1

export OMP_NUM_THREADS=1

source /work/d435/d435/shared/spack/share/spack/setup-env.sh
spack env activate moap
srun --distribution=block:block --hint=nomultithread gungho configuration.nml

