from mpi4py import MPI

comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
rank = comm.Get_rank()

def run_master():
    pass

def run_worker():
    pass

if rank == 0:
    run_master()
else:
    run_slave()

