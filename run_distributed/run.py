from mpi4py import MPI
from run_master import *
from run_worker import *
import argparse
#import nevergrad as ng

from score_dofs import *

parser = argparse.ArgumentParser(description='test_narrowness.py')
parser.add_argument('--opt', help='optimizer to use', required=True )
parser.add_argument('--budget', help='budget for optimizer', required=True, type=int )
parser.add_argument('--hours', help='How long to run the simulation (budget just needs to be an estimate)', required=False, type=float, default=-1.0 )
parser.add_argument('--out_prefix', help='prefix_for_output_files', required=True, type=str )
parser.add_argument('--in_prefices', help='comma separated list of prefices to load from', required=False, type=str, default="" )
args = parser.parse_args()

comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    print( args.opt )
    run_master( comm=comm, nprocs=nprocs, rank=rank, opt=args.opt, budget=args.budget, out_prefix=args.out_prefix, in_prefices=args.in_prefices )
else:
    run_worker( comm, rank, out_prefix=args.out_prefix )

