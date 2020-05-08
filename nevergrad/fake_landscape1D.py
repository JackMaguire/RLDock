#import numpy as np
from random import *
#import math

class FakeLandscape1D:
    #This landscape will have multiple minima of random depths

    def __init__(self):
        #min and max values for minima
        self.min = -100.0
        self.max = 100.0
        self.scale = 100.0 #we want to stay between 0 and 100

        #define min and max depths for the wells
        #(max means more negative, I suppose)
        self.max_depth = -1
        self.min_depth = -0.5

        self.n_minima = 3
        self.minima = []
        self.minima_depths = []
        self.minima_factor = [] #make the wells more shallow
        for i in range( 0, self.n_minima ):
            self.minima.append( uniform( self.min, self.max ) )
            self.minima_depths.append( uniform( self.max_depth, self.min_depth ) )
            self.minima_factor.append( uniform( 0.01, 0.1 ) )

    #arr is a numpy array with shape (1)
    def score( self, arr ):
        #scale
        #val := {-1,1}
        #landscape := {-100,00}
        val = arr[ 0 ] * 100

        #let's just do a simple quadratic to the closest well
        #Energy wells are negative, let's say the lanscape is flat at +1
        best_score = 1
        for i in range( 0, self.n_minima ):
            quardtratic = (abs( val - self.minima[ i ] ) * self.minima_factor[ i ]) ** 2
            score = quardtratic + self.minima_depths[ i ]
            if score < best_score:
                best_score = score
        return best_score

    def print_landscape(self):
        i = self.min / self.scale
        max = self.max / self.scale
        d = 1.0 / self.scale
        while i <= max:
            print( i, self.score( [i] ) )
            i += d

if __name__ == '__main__':
    landscape = FakeLandscape1D()
    landscape.print_landscape()
