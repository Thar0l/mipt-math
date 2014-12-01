'''
Created on Nov 24, 2014

@author: thar0l
'''
from numpy import prod
import pylab
from matplotlib import mlab
from math import *
from tabulate import tabulate

class Polinom(object):
    def __init__(self, size, points, values):
        self.size = size
        self.points = points
        self.values = values
    
    
    def create(self):
        pass
    
    
    def calc(self, x):
        pass



class Polinom_N(Polinom):
    def __init__(self, size, points, values):
        self.size = size
        self.points = points
        self.values = values
        self.table = []
        self.coefs = []

    
    def print_table(self):
        for line in self.table:
            print line

    
    def f(self, count, start):
        if count == 1.0:
            return self.values[start]
        else:
            return (self.table[count-2][start+1] - self.table[count-2][start]) / float(self.points[start+count-1] - self.points[start])

    
    def create(self):
        self.table = [[] for t in range(0, self.size)];  # @UnusedVariable
        for i in range(0, self.size):
            self.table[i] = [0 for t in range(0,self.size - i)]  # @UnusedVariable
            
        for i in range(0, self.size):
            for j in range (0, len(self.table[i])):
                self.table[i][j] = self.f(i+1,j)
        for i in range(0, self.size):
            self.coefs.append(self.table[i][0])

        
    def calc(self, x):
        result = 0.0
        for i in range (0, self.size):
            prod = 1;
            for j in range(0, i):
                prod *= (x-self.points[j])
            result += self.coefs[i] * prod
        return result
    
    
    
class Polinom_L(Polinom):
    def __init__(self, size, points, values):
        self.size = size
        self.points = points
        self.values = values
        self.table = []


    def calc(self, x):
        result = 0.0
        for i in range (0, self.size):
            prod = 1;
            for j in range(0, self.size):
                if (j != i):
                    prod *= (x-self.points[j])/(self.points[i] - self.points[j])
            result += self.values[i] * prod
        return result   

   
    
class SplineTuple(object):
    def __init__(self, a,b,c,d,x):
        self.a =a
        self.b = b
        self.c = c
        self.d = d
        self.x = x
   
   
        
class CubicSplines(Polinom):
    def __init__(self, size, points, values):
        self.size = size
        self.points = points
        self.values = values
        self.splines = []


    def create(self):
        for i in range(0, self.size):
            spline = SplineTuple(self.values[i], 0.0, 0.0, 0.0, self.points[i])
            self.splines.append(spline)
        alpha = [0.0]
        beta = [0.0]
        for i in range(1, self.size-1):
            hi  = self.points[i] - self.points[i - 1]
            hi1 = self.points[i + 1] - self.points[i]
            A = hi
            C = 2.0 * (hi + hi1)
            B = hi1
            F = 6.0 * ((self.values[i + 1] - self.values[i]) / hi1 - (self.values[i] - self.values[i - 1]) / hi)
            z = (A * alpha[i - 1] + C)
            alpha.append(-B / z)
            beta.append((F - A * beta[i - 1]) / z)
            
        self.splines[self.size - 1].c = (F - A * beta[self.size - 2]) / (C + A * alpha[self.size - 2]);
        
        for i in range(self.size-2, 0, -1):
            self.splines[i].c = alpha[i] * self.splines[i + 1].c + beta[i]
        for i in range(self.size-1, 0, -1):
            hi = self.points[i] - self.points[i - 1]
            self.splines[i].d = (self.splines[i].c - self.splines[i - 1].c) / hi
            self.splines[i].b = hi * (2.0 * self.splines[i].c + self.splines[i - 1].c) / 6.0 + (self.values[i] - self.values[i - 1]) / hi

    
    def calc(self, x):
        n = len(self.splines)
        s = SplineTuple(0.0, 0.0, 0.0, 0.0, 0.0)
        if x <= self.splines[0].x:
            s = self.splines[0]
        elif x >= self.splines[n-1].x:
            s = self.splines[n-1]
        else:
            i = 0
            j = n-1
            while (i+1) < j:
                k = i + (j - i) / 2;
                if x <= self.splines[k].x:
                    j = k
                else:
                    i = k
            s = self.splines[j]
        dx = x - s.x
        return s.a + (s.b + (s.c / 2.0 + s.d * dx / 6.0) * dx) * dx;
        

f =  lambda x:  sin(x)   
    
start = 0
end = 16

xpoints = mlab.frange(start, end, 2)
ypoints = [f(x) for x in xpoints]

xlist = mlab.frange(start, end, 0.05)
yreal = [f(x) for x in xlist]

n = Polinom_N(len(xpoints), xpoints, ypoints)
n.create()
y_n = [n.calc(x) for x in xlist]

l = Polinom_L(len(xpoints), xpoints, ypoints)
l.create()
y_l = [l.calc(x) for x in xlist]

s = CubicSplines(len(xpoints), xpoints, ypoints)
s.create()
y_s = [s.calc(x) for x in xlist]


diff_n = [abs(y2 - y1) for y1, y2 in zip(yreal, y_n)]
diff_l = [abs(y2 - y1) for y1, y2 in zip(yreal, y_l)]
diff_s = [abs(y2 - y1) for y1, y2 in zip(yreal, y_s)]
diff_nl = [abs(y2 - y1) for y1, y2 in zip(y_n, y_l)]
zeros = [0.0 for x in xlist]


print tabulate({"x": xlist, "y_Real": yreal, "y_Newton": y_n, "y_Lagrange": y_l, "y_Splines": y_s}, headers="keys", tablefmt="grid")

pylab.figure(1)
pylab.subplot(311)
pylab.title("f(x)")
plot_points = pylab.plot(xpoints, ypoints, "o")
plot_real = pylab.plot(xlist, yreal, label = "yreal")
plot_n = pylab.plot(xlist, y_n, label = "y_n")
plot_l = pylab.plot(xlist, y_l, label = "y_l")
plot_s = pylab.plot(xlist, y_s, label = "y_s")
pylab.setp(plot_points, color = 'black')
pylab.setp(plot_real, color = 'black')
pylab.setp(plot_n, color = 'red')
pylab.setp(plot_l, color = 'green')
pylab.setp(plot_s, color = 'blue')
pylab.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)

pylab.subplot(312)
pylab.title("diff(x)")
plot_diffn = pylab.plot(xlist, diff_n, label = "| yreal - y_n |")
plot_diffl = pylab.plot(xlist, diff_l, label = "| yreal - y_l |")
plot_diffs = pylab.plot(xlist, diff_s, label = "| yreal - y_s |")
pylab.setp(plot_diffn, color = 'red')
pylab.setp(plot_diffl, color = 'green')
pylab.setp(plot_diffs, color = 'blue')
pylab.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)

pylab.subplot(313)
pylab.title("diff(x)")
plot_diffnl = pylab.plot(xlist, diff_nl,label = "| y_l - y_n |")
pylab.setp(plot_diffnl, color = 'black')
pylab.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)


pylab.show()