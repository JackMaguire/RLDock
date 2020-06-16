from fake_landscape import *
import nevergrad as ng
import matplotlib.pyplot as plt
from numpy import mean
import numpy as np
import random as rand
import argparse
import matplotlib.cm as cm
from matplotlib.animation import FuncAnimation

parser = argparse.ArgumentParser(description='test_narrowness.py')
parser.add_argument('--opt', help='optimizer to use', required=True )
args = parser.parse_args()

print( args.opt )

#opt=args.opt
np.random.seed( 3 )
rand.seed( a=3 )
landscape = FakeLandscape( 2, width_factor=8.0 )

#landscape.score( [0,0] )

#https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/contour_demo.html

delta = 0.01
x = np.arange(-2.0, 2.0, delta)
y = np.arange(-2.0, 2.0, delta)
X, Y = np.meshgrid(x, y)

#ugly but gives us the right dimensions
Z = np.exp(-X**2 - Y**2)
for i in range( 0, len(x) ):
    for j in range( 0, len(y) ):
        Z[i][j] = landscape.score( [ x[i], y[j] ], noise=False )


fig, ax = plt.subplots()
CS = ax.contour(X, Y, Z, levels=50, zorder=0 )
fig.savefig( "contour_movie.pdf" )

#relevant links:
# - https://stackoverflow.com/questions/55624400/animate-scatter-and-contour-plot

scatter_X_points = []
scatter_Y_points = []
npoints=300
nworkers=5
optimizer = ng.optimizers.registry[ args.opt ]( parametrization=2, budget=npoints, num_workers=nworkers )
for _ in range( 0, npoints ):
    asked = optimizer.ask();
    scatter_X_points.append( asked.value[1] )
    scatter_Y_points.append( asked.value[0] )
    score = landscape.score( asked.value, noise=True )
    optimizer.tell( asked, score )

scat = ax.scatter( scatter_X_points[0:nworkers], scatter_Y_points[0:nworkers], c="#000000", zorder=1 )

fig.savefig( "contour_movie.inital_points.pdf" )

def animate(i):
    x_i = scatter_X_points[i:nworkers+i]
    y_i = scatter_Y_points[i:nworkers+i]
    scat.set_offsets( np.c_[ x_i, y_i ] )

anim = FuncAnimation(
    fig, animate, interval=100, frames=npoints-nworkers-1)

#This needs you to install ffmpeg
anim.save( args.opt + 'contour.mp4' )
