#!/bin/bash

#SBATCH --time=3-0:00:00
#SBATCH -p skylake,528_queue
#SBATCH -N 2
#SBATCH --ntasks-per-node=40
#SBATCH -o OUT.%j.log

#aiming for 6 * 572 = 3432 CPU Hours

# 80 CPUs -> 42.9 hours
# 120 CPUs -> 28.6 hours
# 160 CPUs -> 21.45 hours

optimizer="RealSpacePSO"
nCPU="80"
hours="42.9"

outdir="$optimizer.$nCPU.$hours.out"
mkdir $outdir

#mpirun -np $nCPU --oversubscribe
srun --mpi=pmi2 -n $nCPU python3 run.py --opt $optimizer --budget 1000000 --out_prefix "$outdir/out" --hours $hours

#1) mvapich2_2.3a/gcc_4.8.5   2) python/3.6.6
# git clone https://p:ft@graylab.jhu.edu/download/PyRosetta4/git/release/PyRosetta4.Release.python36.linux.release.git

# sbatch submit.sh
