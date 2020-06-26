#!/bin/bash

#SBATCH --time=3-0:00:00
#SBATCH -p skylake,528_queue
#SBATCH -N 2
#SBATCH --ntasks-per-node=40
#SBATCH -o OUT.%j.log

#aiming for 6 * 572 = 3432 CPU Hours

# 80 CPUs -> 42.9 hours

optimizer="PSO"
nCPU="80"
hours="42.9"

outdir="$optimizer.$nCPU.$hours.out"
mkdir $outdir

#mpirun -np $nCPU --oversubscribe
srun --mpi=mpi2 -n $nCPU python3 run.py --opt $optimizer --budget 1000000 --out_prefix "$outdir/out" --hours $hours
