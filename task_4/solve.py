#!/usr/bin/python

import argparse
import numpy
import matplotlib.pyplot
from math import *


#####################################################################################
#    y'' - 0.5y'/(x-1) = 20sqrt(x-1)/4, 2 <= x <= 5, y'(2) = 0, y(5) - 2y'(5) = 0    #
#####################################################################################

a = 2.0
b = 5.0

###############
# 0 1 2 3 4 5 #
###################
# b c         # 0 #
# a b c       # f #
#   a b c     # f #
#     a b c   # f #
#       a b c # f #
#         a b # 0 #
###################


# https://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm - solving algorithm

def Solve(a, b, c, d):
    n = len(a)    
    _a, _b, _c, _d = map(numpy.array, (a, b, c, d))     
    for i in xrange(1, n):
        mc = _a[i]/_b[i-1]
        _b[i] = _b[i] - mc*_c[i-1] 
        _d[i] = _d[i] - mc*_d[i-1]
 
    xc = _a
    xc[-1] = _d[-1]/_b[-1]
 
    for i in xrange(n-2, -1, -1):
        xc[i] = (_d[i]-_c[i]*xc[i+1])/_b[i]
 
    del _b, _c, _d  
    return xc 



def _f(x):
    #return 19.375+1.25*sqrt(x-1)*x*x-2.5*sqrt(x-1)*x + 1.25*sqrt(x-1) - 6.25*x/sqrt(x-1) + 6.25/sqrt(x-1)
    #return 1.25*sqrt(x+1)*x*x+2.5*sqrt(x+1)*x-56.25*x/sqrt(x+1)+1.25*sqrt(x+1)-56.25/sqrt(x+1)+96.4487
    return 15.5 - 5 * sqrt(x - 1) + ((sqrt(x - 1))**5)

######################
# y'' + py' + qy = f #
######################

def q(x):
    return 0



def p(x):
    return 0.5 / (x - 1)



def f(x):
    return 20 * sqrt(x - 1) / 4


#########
# Begin #
#########

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--count", help="Iterations count", type = int)
args = parser.parse_args() 
if args.count:
    N = args.count
else:
    N = 10

h = (b - a)/float(N)
X = [a + i * h for i in xrange(N+1)]

print ("h = " + str(h))

b = [-2.0 + h**2 * q(X[i]) for i in range(1, N, 1)]
c = [1.0 + p(X[i]) * h / 2.0 for i in range(1, N-1, 1)]
a = [1.0 - p(X[i]) * h / 2.0 for i in range(2, N, 1)]
f = [h**2 * f(X[i]) for i in range(1, N, 1)]

# Right
a += [2.0 / h]
b += [1.0 - 2.0 / h]
c += [1.0 + p(X[N - 1]) * h / 2.0]
f += [.00]

# Left
a = [1.0 - p(X[1]) * h / 2.0] + a
b = [-1 / h] + b
c = [1 / h] + c
f = [0.0] + f

# Align
a = [0.0] + a
c += [0.0]

#Solving
Y = Solve(a, b, c, f).tolist()
Y_ = [_f(x) for x in X]

#Plots
matplotlib.pyplot.plot(X, Y, 'bo')
matplotlib.pyplot.plot(X, Y, 'b')
matplotlib.pyplot.plot(X, Y_, 'go')
matplotlib.pyplot.plot(X, Y_, 'g')
matplotlib.pyplot.show()