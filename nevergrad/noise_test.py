# test.py
from fake_landscape import *
import nevergrad as ng
import matplotlib.pyplot as plt
from numpy import mean
'''
for x in ng.optimizers.registry:
    print( x )
exit(0)
'''
def run( ndim, budget, landscape, opt_name ):
    def measure( x ):
        return landscape.score( x )

    #TBPSA
    #PSO
    #ScrHammersleySearchPlusMiddlePoint
    optimizer = ng.optimizers.registry[ opt_name ]( parametrization=ndim, budget=budget, num_workers=1000 )
    recommendation = optimizer.minimize( measure )

    best_score_found = landscape.score( recommendation.value, noise=False )
    score = best_score_found / landscape.global_minimum
    return score

X = []
TBPSA = []
PSO = []
SCR = []

noise = 0.01
while noise <= 0.5:
    budget=1000
    
    TBPSA_scores = []
    PSO_scores = []
    SCR_scores = []
    for r in range( 0, 10 ): #TODO 10
        print( noise, ", round", r, "/ 10" )
        landscape = FakeLandscape( 6, noise )
        TBPSA_scores.append( run( 6, budget, landscape, "TBPSA" ) )
        PSO_scores.append( run( 6, budget, landscape, "PSO" ) )
        SCR_scores.append( run( 6, budget, landscape, "ScrHammersleySearchPlusMiddlePoint" ) )
    
    X.append( noise )
    TBPSA.append( mean( TBPSA_scores ) )
    PSO.append( mean( PSO_scores ) )
    SCR.append( mean( SCR_scores ) )
    noise = noise * 2 # TODO 2

plt.plot( X, TBPSA, label="TBPSA" )
plt.plot( X, PSO, label="PSO" )
plt.plot( X, SCR, label="SCR" )
plt.legend()
plt.xlabel( "Noise Levels" )
plt.ylabel( "Sampling Quality" )
plt.savefig("test.noise.pdf", bbox_inches='tight')
