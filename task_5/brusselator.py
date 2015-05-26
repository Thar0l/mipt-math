from matplotlib import pyplot as plt
import math

def calculator( a, b, d1, d2, dt, h, l):

    def dot_x( x, y , xl, xr):
        return a + x * x * y - (b + 1) * x + d1 / (h* h) * (xl -2 * x + xr)

    def dot_y( x, y , yl, yr):
         return b * x - x * x * y + d2 / (h* h) * (yl -2 * y + yr)

    n = int(l / h)

    count = 16000
    
    X = [[0 for j in range(count)] for i in range(n)]
    Y = [[0 for j in range(count)] for i in range(n)]

    for i in range(n):
        X[i][0] = a * (1.0 + 1.0 * math.cos (1.0 * i * h))
        Y[i][0] = b / a

    for i in range(1, count):
        for j in range(1, n-1):
            X[j][i] = X[j][i - 1] + dot_x(X[j][i - 1], Y[j][i - 1], X[j - 1][i - 1], X[j + 1][i - 1]) * dt
            Y[j][i] = Y[j][i - 1] + dot_y(X[j][i - 1], Y[j][i - 1], Y[j - 1][i - 1], Y[j + 1][i - 1]) * dt
        X[0][i] = X[1][i]
        Y[0][i] = Y[1][i]
        X[n - 1][i] = X[n - 1][i]
        Y[n - 1][i] = Y[n - 1][i]
    return X, Y

l = 1.0
t = 1e-3
h = 1e-1
d1 = 0.0
d2 = 0.0
a = 1.0
b = 2.0

print a*math.sqrt(d1*d2)
print (1+a*math.sqrt(d1*d2)) ** 2
n = int(l / h)

X, Y = calculator(a, b, d1, d2, t, h, l)

x = []
y = []

print n

for i in range(0, n):
    x.append(X[i][12000])
    y.append(Y[i][12000])

plt.plot(X[int(n/2)], Y[int(n/2)])
plt.show()
plt.cla()

t = [1e-2 * i for i in range(len(X[0]))]
p1 = plt.plot(t, X[int(n/2)])
p2 = plt.plot(t, Y[int(n/2)])
plt.show()
'''plt.cla()

t = [h * i for i in range(len(x))]
p1 = plt.plot(t, x)
p2 = plt.plot(t, y)

plt.show()
'''

'''
from matplotlib import pyplot as plt

def calculator( a, b, x0, y0, d1, d2, dt, h, l):

    def dot_x( x, y , xl, xr):
        return a + x * x * y - (b + 1) * x + d1 / (h* h) * (xl -2 * x + xr)

    def dot_y( x, y , yl, yr):
         return b * x - x * x * y + d2 / (h* h) * (yl -2 * y + yr)
    
    X, Y = [], []

    x = x0
    y = y0

    count = 5000

    for i in range(count):
        X.append(x)
        Y.append(y)
        x = x + dot_x(x, y, 0, 0) * dt
        y = y + dot_y(x, y, 0, 0) * dt 
    return X, Y

x, y = calculator( 1.0, 1.7, 1.0, 1.0, 0.0, 0.0, 1e-2, 1e-1, 1.0)
plt.plot(x, y)
plt.show()
plt.cla()
t = [1e-2 * i for i in range(len(x))]
p1 = plt.plot(t, x)
p2 = plt.plot(t, y)
plt.legend([p1, p2], ["x", "y"], loc=2)
plt.show()
'''