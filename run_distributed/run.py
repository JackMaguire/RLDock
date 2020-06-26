from mpi4py import MPI
from run_master import *
import argparse
#import nevergrad as ng

from score_dofs import *

parser = argparse.ArgumentParser(description='test_narrowness.py')
parser.add_argument('--opt', help='optimizer to use', required=True )
parser.add_argument('--budget', help='budget for optimizer', required=True, type=int )
parser.add_argument('--out_prefix', help='prefix_for_output_files', required=True, type=str )
parser.add_argument('--in_prefices', help='comma separated list of prefices to load from', required=False, type=str, default="" )
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

def run_worker( comm, rank, out_prefix ):

    dumped_pose_count = 0;
    
    while True:
        status = MPI.Status()
        six_dofs = comm.recv( source=0, tag=MPI.ANY_TAG, status=status )
        if status.Get_tag() == 0:
            comm.send( 0, dest=0, tag=0 )
            #print( "Dying" )
            break

        #print( "Running", six_dofs.value )
        score_pose_dict = score_separate_dofs_and_get_pose( t=six_dofs.value[1]['t'], r=six_dofs.value[1]['r'] )
        
        pose_filename="(none)"
        if "pose" in score_pose_dict:
            dumped_pose_count += 1
            pose_filename = out_prefix + "_" + str( rank ) + "_" + str( dumped_pose_count ) + ".pdb"
            score_pose_dict[ "pose" ].dump_pdb( pose_filename )
            
        assert( "score" in score_pose_dict )
        score = score_pose_dict[ "score" ]
        
        bundle = [ six_dofs, score, pose_filename ]
        comm.send( bundle, dest=0, tag=1 )

if rank == 0:
    run_master( comm=comm, nprocs=nprocs, rank=rank, opt=args.opt, budget=args.budget, out_prefix=args.out_prefix, in_prefices=args.in_prefices )
else:
    run_worker( comm, rank, out_prefix=args.out_prefix )

