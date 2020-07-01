from score_dofs import *
import nevergrad as ng
import argparse

parser = argparse.ArgumentParser(description='test_narrowness.py')
parser.add_argument('--opt', help='optimizer to use', required=True )
args = parser.parse_args()

print( args.opt )

TransParams = ng.p.Array( shape=(3,) )
RotParams = ng.p.Array( shape=(3,) ).set_bounds( -2.5, 2.5 )
AllParams = ng.p.Instrumentation( t=TransParams, r=RotParams )

optimizer = ng.optimizers.registry[ args.opt ]( parametrization=AllParams, budget=10000, num_workers=1000 )
recommendation = optimizer.minimize( score_separate_dofs )
print( recommendation.value )

