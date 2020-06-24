from score_dofs import *
import nevergrad as ng
#print( score_dofs( [0.1,0,0,0,0,0] ) )
"""
TransParams = ng.p.Array( shape=(3,) )
RotParams = ng.p.Array( shape=(3,) ).set_bounds( -1.25, 1.25 )
AllParams = ng.p.Instrumentation( TransParams, RotParams )

optimizer = ng.optimizers.registry[ "PSO" ]( parametrization=AllParams, budget=100, num_workers=1 )
recommendation = optimizer.minimize( score_separate_dofs )
print( recommendation.value )
print( score_separate_dofs( recommendation.value ) )\
"""
#print( score_dofs( [ 0.24034712, -0.26915424, -0.38369293,  0.30019644, -0.05951289, -1.03658494] ) )

print( score_separate_dofs( [0.16773531, 1.19820381, 0.31653974], [ 0.4517856 , -1.16624596,  0.17707031] ) )
print( score_separate_dofs( [ 0, 0, 0 ], [ 0, 0, 0 ] ) )

