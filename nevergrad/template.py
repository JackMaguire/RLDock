from fake_landscape import *
import nevergrad as ng
import matplotlib.pyplot as plt
from numpy import mean
import numpy as np
import random as rand
import argparse

parser = argparse.ArgumentParser(description='test_narrowness.py')
parser.add_argument('--opt', help='optimizer to use', required=True )
args = parser.parse_args()

print( args.opt )

def run( landscape, opt_name, num_workers=1000, budget=10000, ndim=6 ):
    def measure( x ):
        return landscape.score( x, noise=True )

    optimizer = ng.optimizers.registry[ opt_name ]( parametrization=ndim, budget=budget, num_workers=num_workers )
    recommendation = optimizer.minimize( measure )
    best_score_found = landscape.score( recommendation.value, noise=False )
    score = best_score_found / landscape.global_minimum
    return score


opt=args.opt
print( "noise", opt )


noise = 0.01
while noise <= 0.5:
    budget=10000 #benchmark at 10000
    
    scores = []
    for r in range( 0, 10 ): #Keep at 10
        np.random.seed( r )
        rand.seed( a=r )
        #print( noise, ", round", r, "/ 10" )
        landscape = FakeLandscape( 6, noise )
        score = run( landscape, opt, budget=budget )
        scores.append( score )

    score_mean = mean( scores )
    score_std = np.std( scores )
    print( noise, score_mean, score_std )
    
    noise = noise * 2
