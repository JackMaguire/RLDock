from fake_landscape import *
import nevergrad as ng
import matplotlib.pyplot as plt
from numpy import mean
import numpy as np
import random as rand
import argparse

parser = argparse.ArgumentParser(description='test_narrowness.py')
parser.add_argument('--opt', help='sum the integers (default: find the max)', required=True )
args = parser.parse_args()

print( args.opt )
exit( 0 )

def run( landscape, opt_name, num_workers=1000, budget=10000, ndim=6 ):
    def measure( x ):
        return landscape.score( x, noise=True )

    optimizer = ng.optimizers.registry[ opt_name ]( parametrization=ndim, budget=budget, num_workers=num_workers )
    recommendation = optimizer.minimize( measure )
    best_score_found = landscape.score( recommendation.value, noise=False )
    score = best_score_found / landscape.global_minimum
    return score


print( "width_factor", args.opt )


width_factor = 1.0
while width_factor <= 128:
    budget=10000 #benchmark at 10000
    
    scores = []
    for r in range( 0, 10 ): #benchmark at 10
        np.random.seed( r )
        rand.seed( a=r )
        #print( width_factor, ", round", r, "/ 10" )
        landscape = FakeLandscape( width_factor=width_factor )
        score = run( landscape, args.opt, budget=budget )
        scores.append( score )

    score_mean = mean( scores )
    score_std = np.std( scores )
    print( width_factor, score_mean, score_std )
    
    width_factor = width_factor * 2
