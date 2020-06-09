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
def run( ndim, budget ):
    landscape = FakeLandscape( ndim )

    #i = 0
    Xs = []
    Ys = []
    
    def measure( x ):
        #global i
        myscore = landscape.score( x );
        #i = i + 1
        Xs.append( len(Xs)-1 )
        Ys.append( myscore / landscape.global_minimum )
        return myscore

    #TBPSA
    #PSO
    #ScrHammersleySearchPlusMiddlePoint
    optimizer = ng.optimizers.OnePlusOne( parametrization=ndim, budget=budget, num_workers=1000 )
    recommendation = optimizer.minimize( measure )

    best_score_found = landscape.score( recommendation.value, noise=False )
    score = best_score_found / landscape.global_minimum
    return Xs, Ys


Xs, Ys = run( 6, 10000 )

Y2s = []

best_score = Ys[ 0 ]
Y2s.append( best_score )
for i in range( 1, len( Ys ) ):
    if Ys[ i ] > best_score:
        best_score = Ys[ i ]
    Y2s.append( best_score )
    


plt.plot( Xs, Ys )
plt.plot( Xs, Y2s )
plt.xlabel( "Sample Num" )
plt.ylabel( "Score" )
plt.ylim(0.99,1.0)
plt.savefig("test2.pdf", bbox_inches='tight')
