from mpi4py import MPI
from run_master import *
import argparse
#import nevergrad as ng

parser = argparse.ArgumentParser(description='test_narrowness.py')
parser.add_argument('--opt', help='optimizer to use', required=True )
parser.add_argument('--budget', help='budget for optimizer', required=True, type=int )
args = parser.parse_args()

print( args.opt )


comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
rank = comm.Get_rank()

def scorer(x):
    mysum = 0
    for i in x:
        mysum += i*i
    return mysum

def run_slave( comm, rank ):

    while True:
        status = MPI.Status()
        six_dofs = comm.recv( source=0, tag=MPI.ANY_TAG, status=status )
        if status.Get_tag() == 0:
            comm.send( 0, dest=0, tag=0 )
            print( "Dying" )
            break

        #print( "Running", six_dofs.value )
        score = scorer( six_dofs.value )
        pose_filename = "test"
        bundle = [ six_dofs, score, pose_filename ]
        comm.send( bundle, dest=0, tag=1 )

if rank == 0:
    run_master( comm=comm, nprocs=nprocs, rank=rank, opt=args.opt, budget=args.budget )
else:
    run_slave( comm, rank )

