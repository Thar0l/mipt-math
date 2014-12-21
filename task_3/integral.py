import numpy
import pylab

def f(arr):
    result = 1.0
    for item in arr: result *= item
    return result

start = 0.0
end = 1.0  
dimensions = 10
res = 0.0
n = 1000000
runs = 5

for a in range(0, runs):    
    arr = [] 
    res = 0.0
    points = [numpy.random.uniform(start, end, dimensions) for i in range(0, n)]
    for i in range(1,n):
        flag = True
        for p in points[i]: 
            if p < start or p > end: 
                flag = False
        if flag:
            res += f(points[i])
            arr.append(res * ((end - start)**dimensions) /i)
    print a, "\t:\t", a*100/runs, "%", "\t:\t", res * ((end - start)**dimensions) /n
    x = [i for i in range(1,n)]
    pylab.plot(x[10::], arr[10::])
    if a == 0:
        pylab.plot(x, arr)
print "******************************************"
print "Final\t:\t", res * ((end - start)**dimensions) /n
pylab.show()