from mpi4py import MPI
from score_dofs import *

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

        count_against_budget = score_pose_dict[ "ran_fast_design" ]
        
        bundle = [ six_dofs, score, pose_filename, count_against_budget ]
        comm.send( bundle, dest=0, tag=1 )
