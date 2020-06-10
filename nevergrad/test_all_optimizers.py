from fake_landscape import *
import nevergrad as ng
import matplotlib.pyplot as plt
from numpy import mean
import numpy as np
import random as rand
from concurrent import futures

def run( landscape, opt_name, num_workers=1000, budget=10000, ndim=6 ):
    def measure( x ):
        return landscape.score( x, noise=True )

    optimizer = ng.optimizers.registry[ opt_name ]( parametrization=ndim, budget=budget, num_workers=num_workers )

    with futures.ThreadPoolExecutor( max_workers=2 ) as executor:
        recommendation = optimizer.minimize( measure, executor=executor )
    #recommendation = optimizer.minimize( measure )

    best_score_found = landscape.score( recommendation.value, noise=False )
    score = best_score_found / landscape.global_minimum
    #print( recommendation.value )
    return score


# Print score if you always guess [ 0, 0, ... 0 ]
scores = []
for r in range( 0, 10 ): #Keep at 10
    np.random.seed( r )
    rand.seed( a=r )
    #print( noise, ", round", r, "/ 10" )
    landscape = FakeLandscape( 6, 0.05 ) #6 dim, noise=0.05
    score = landscape.score( [0,0,0,0,0,0], noise=False ) / landscape.global_minimum
    scores.append( score )

score_mean = mean( scores )
score_std = np.std( scores )
print( "control", score_mean, score_std )

#make a list of all optimizers
all_opts = []
for opt in ng.optimizers.registry:
    all_opts.append( opt )

# Loop over all optimizers
for i in range( 0, 10 ): # 84 elements
    opt = all_opts[ i ]
    
    try:
        budget=10000 #benchmark at 10000
    
        scores = []
        for r in range( 0, 10 ): #Keep at 10
            np.random.seed( r )
            rand.seed( a=r )
            #print( noise, ", round", r, "/ 10" )
            landscape = FakeLandscape( 6, 0.05 ) #6 dim, noise=0.05
            score = run( landscape, opt, budget=budget )
            scores.append( score )

        score_mean = mean( scores )
        score_std = np.std( scores )
        print( opt, score_mean, score_std )
    except:
        print( opt, " failed" )
