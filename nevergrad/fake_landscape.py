#import numpy as np
from random import *
import math

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

def add_noise( score ):
    one_percent = score * 0.1
    noise = uniform( - one_percent, one_percent )
    return score * ( 1 + noise )

class FakeLandscape:
    #This landscape will have multiple minima of random depths

    def __init__(self, ndim):
        self.ndim = ndim #Expecting 1 to 6 dimensions

        #min and max values for minima
        self.min = -100.0
        self.max = 100.0
        self.scale = 100.0 #we want to stay between 0 and 100

        #define min and max depths for the wells
        #(max means more negative, I suppose)
        self.max_depth = -1
        self.min_depth = -0.5

        self.n_minima = 3 ** self.ndim
        self.minima = [] #each element is an array
        self.minima_depths = []
        self.minima_factor = [] #make the wells more shallow
        for i in range( 0, self.n_minima ):
            minima_coords = []
            for _ in range( 0, self.ndim ):
                minima_coords.append( uniform( self.min, self.max ) )

            self.minima.append( minima_coords )
            self.minima_depths.append( uniform( self.max_depth, self.min_depth ) )
            self.minima_factor.append( uniform( 0.01, 0.1 ) )

    #arr is a numpy array with shape (self.ndim)
    def score( self, arr ):
        #scale
        #arr := {-1,1}
        #landscape := {-100,00}
        vals = []
        for a in arr:
            vals.append( a * self.scale )

        #let's just do a simple quadratic to the closest well
        #Energy wells are negative, let's say the lanscape is flat at +1
        best_score = 1
        for i in range( 0, self.n_minima ):
            distance = 0
            for j in range( 0, self.ndim ):
                distance += (vals[ j ] - self.minima[ i ][ j ]) ** 2
            distance = math.sqrt( distance )

            quardtratic = ( distance * self.minima_factor[ i ] ) ** 2
            score = quardtratic + self.minima_depths[ i ]
            if score < best_score:
                best_score = score
        return add_noise( best_score )

if __name__ == '__main__':
    #print 2D landscape
    landscape = FakeLandscape( 2 )

    min = 1.5 * ( landscape.min / landscape.scale )
    max = 1.5 * ( landscape.max / landscape.scale )
    d = 1.0 / landscape.scale

    x = np.arange(min,max,d)
    y = np.arange(min,max,d)
    X,Y = np.meshgrid(x,y)
    Z = X*np.exp(-X-Y)

    for i in range( 0, len(x) ):
        for j in range( 0, len(y) ):
            Z[i][j] = landscape.score( [ x[i], y[j] ] )

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z)
    plt.show()
