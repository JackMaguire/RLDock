from itertools import combinations
import sys

for combo in combinations( sys.argv[1:], 4 ):
    print( combo[0], combo[1], combo[2], combo[3] )
