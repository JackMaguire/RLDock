from mpi4py import MPI
#from sets import Set
import nevergrad as ng
import numpy as np

all_results_tdofs = []
all_results_rdofs = []
all_results_scores = []

def send_job_to_node( comm, six_dofs, node, tag=1 ):
    comm.send( six_dofs, dest=node, tag=tag )

def interpret_result( bundle ):
    six_dofs = bundle[ 0 ]
    score = bundle[ 1 ]
    pose_filename = bundle[ 2 ]
    print( "RESULT", pose_filename, score, six_dofs )

    all_results_tdofs.append( np.asarray( six_dofs.value[1]['t'] ) )
    all_results_rdofs.append( np.asarray( six_dofs.value[1]['r'] ) )
    all_results_scores.append( np.asarray( score ) )

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
def run_master( comm, nprocs, rank, opt, budget, out_prefix, in_prefices ):
    
    available_nodes = set()
    for i in range( 1, nprocs ):
        available_nodes.add( i )

    working_nodes = set()

    TransParams = ng.p.Array( shape=(3,) )
    RotParams = ng.p.Array( shape=(3,) ).set_bounds( -2.5, 2.5 )
    AllParams = ng.p.Instrumentation( t=TransParams, r=RotParams )

    optimizer = ng.optimizers.registry[ opt ]( parametrization=AllParams, budget=budget, num_workers=(nprocs-1) )

    #Load if needed
    if len( in_prefices ) > 0:
        npoints_loaded=0
        for prefix in in_prefices.split( "," ):
            filenamet = prefix + ".all_results_tdofs.npy"
            filenamer = prefix + ".all_results_rdofs.npy"
            filenames = prefix + ".all_results_scores.npy"
            tdofs = np.load( filenamet, allow_pickle=False )
            rdofs = np.load( filenamer, allow_pickle=False )
            score = np.load( filenames, allow_pickle=False )
            assert( len( tdofs ) == len( rdofs ) )
            assert( len( tdofs ) == len( score ) )
            for i in range( 0, len( tdofs ) ):
                #optimizer.suggest( dofs[ i ] )
                #x = optimizer.ask()
                #x = optimizer.parametrization.spawn_child(new_value=( tdofs[ i ], rdofs[i] ))
                x = optimizer.parametrization.spawn_child(new_value=((), {'t': tdofs[ i ], 'r': rdofs[i]}) )
                optimizer.tell( x, score[ i ] )
                npoints_loaded += 1
        print( "loaded", npoints_loaded, "points" )
        
    
    adjusted_budget = budget #this grows when jobs fail
    njobs_sent = 0
    while njobs_sent < adjusted_budget:
    #for b in range( 0, budget ):
        if njobs_sent % 1 == 0:
            print( "Sent", njobs_sent, "jobs from budget of", adjusted_budget )
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
            count_against_budget = bundle[ 3 ]
            if not count_against_budget:
                adjusted_budget += 1
            optimizer.tell( six_dofs, score )

            interpret_result( bundle )
        #end if
        
        six_dofs = optimizer.ask()

        node = available_nodes.pop() #removes node from available_nodes
        send_job_to_node( comm, six_dofs, node )
        working_nodes.add( node )
        njobs_sent += 1

    #end for b    
    execute_kill_seq( comm, available_nodes, working_nodes )
    print( optimizer.provide_recommendation().value )

    test1 = np.asarray( all_results_tdofs )
    print( test1.shape )
    
    np.save( out_prefix + ".all_results_tdofs.npy", np.asarray(all_results_tdofs), allow_pickle=False )
    np.save( out_prefix + ".all_results_rdofs.npy", np.asarray(all_results_rdofs), allow_pickle=False )
    np.save( out_prefix + ".all_results_scores.npy", np.asarray(all_results_scores), allow_pickle=False )
