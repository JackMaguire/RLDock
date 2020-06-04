from mpi4py import MPI

from run_master import *

comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
rank = comm.Get_rank()

def run_slave( comm, rank ):

    pose = whatever()

    while True:
        six_dofs = comm.recv( source=0, tag=11 )
        if is_kill_signal( six_dofs ):
            comm.send( 0, dest=0, tag=0 )
            break
        score, pose_filename = score_six_dofs( six_dofs )
        bundle = [ score, pose_filename ]
        comm.send( bundle, dest=0, tag=11 )

if rank == 0:
    run_master( comm, nprocs, rank )
else:
    run_slave( comm, rank )

