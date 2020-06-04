from mpi4py import MPI
from sets import Set

def send_job_to_node( six_dofs, node ):
    comm.send( six_dofs, dest=node, tag=11 )

def execute_kill_seq( available_nodes, working_nodes ):
    six_dofs = get_kill_signal()

    while len( available_nodes ) > 0:
        node = available_nodes.pop()
        send_job_to_node( six_dofs, node )
        message = comm.recv( source=node, tag=MPI.ANY_TAG )
        if message != 0:
            print( "Node ", node, " sent ", message, " instead of 0 upon kill" )

    while len( working_nodes ) > 0:
        status = MPI.Status()
        bundle = comm.recv( source=MPI.ANY_SOURCE, tag=11, status=status )
        source = status.Get_source()
        working_nodes.remove( source )
        #available_nodes.add( source )

        score = bundle[ 0 ]
        pose_filename = bundle[ 1 ]
        interpret_result( score, pose_filename )

        node = source
        send_job_to_node( six_dofs, node )
        message = comm.recv( source=node, tag=MPI.ANY_TAG )
        if message != 0:
            print( "Node ", node, " sent ", message, " instead of 0 upon kill" )

    exit( 0 )


#https://stackoverflow.com/questions/21088420/mpi4py-send-recv-with-tag
def run_master( comm, nprocs, rank ):
    available_nodes = Set()
    for i in range( 1, nprocs ):
        available_nodes.add( i )

    working_nodes = Set()

    while True:
        while len( available_nodes ) > 0:
            six_dofs = get_next_sample()
            if is_kill_signal( six_dofs ):
                execute_kill_seq( available_nodes, working_nodes )

            node = available_nodes.pop()
            send_job_to_node( six_dofs, node )
            working_nodes.add( node )

        #All are busy, wait for results
        status = MPI.Status()
        bundle = comm.recv( source=MPI.ANY_SOURCE, tag=11, status=status )
        source = status.Get_source()
        working_nodes.remove( source )
        available_nodes.add( source )

        score = bundle[ 0 ]
        pose_filename = bundle[ 1 ]
        interpret_result( score, pose_filename )
