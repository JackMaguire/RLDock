from mpi4py import MPI
#from sets import Set
import nevergrad as ng

def send_job_to_node( comm, six_dofs, node, tag=1 ):
    comm.send( six_dofs, dest=node, tag=tag )

def interpret_result( bundle ):
    six_dofs = bundle[ 0 ]
    score = bundle[ 1 ]
    pose_filename = bundle[ 2 ]
    #TODO

def tell_node_to_die( comm, node ):
    send_job_to_node( comm, "die", node, tag=0 )
    message = comm.recv( source=node, tag=MPI.ANY_TAG )
    if message != 0:
        print( "Node ", node, " sent ", message, " instead of 0 upon kill" )
    
def execute_kill_seq( comm, available_nodes, working_nodes ):

    while len( available_nodes ) > 0:
        node = available_nodes.pop()
        tell_node_to_die( comm, node )
        
    while len( working_nodes ) > 0:
        status = MPI.Status()
        bundle = comm.recv( source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status )
        interpret_result( bundle )
        
        source = status.Get_source()
        working_nodes.remove( source )
        tell_node_to_die( comm, source )

#https://stackoverflow.com/questions/21088420/mpi4py-send-recv-with-tag
def run_master( comm, nprocs, rank, opt, budget ):
    
    available_nodes = set()
    for i in range( 1, nprocs ):
        available_nodes.add( i )

    working_nodes = set()
    
    optimizer = ng.optimizers.registry[ opt ]( parametrization=6, budget=budget, num_workers=(nprocs-1) )
    
    for b in range( 0, budget ):
        if len( available_nodes ) == 0:
            #All are busy, wait for results
            status = MPI.Status()
            bundle = comm.recv( source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status )
            source = status.Get_source()
            working_nodes.remove( source )
            available_nodes.add( source )

            six_dofs = bundle[ 0 ]
            score = bundle[ 1 ]
            pose_filename = bundle[ 2 ]
            optimizer.tell( six_dofs, score )

            interpret_result( bundle )
        #end if
        
        six_dofs = optimizer.ask()

        node = available_nodes.pop() #removes node from available_nodes
        send_job_to_node( comm, six_dofs, node )
        working_nodes.add( node )
    #end for b    
    execute_kill_seq( comm, available_nodes, working_nodes )
    print( optimizer.provide_recommendation().value )
