#!/usr/bin/python
from math import *
import numpy as np
import matplotlib.pyplot as plt
from random import random
from scipy.optimize import root

# Define the transmitter's true location
bx_t=250.; #bx_t = 0.7
by_t=110.; #by_t = 0.37

# Load lat lon pop of Mass. census data and convert to cartesian coords
newarray = np.loadtxt('popgrid.txt')
min_lat, min_lon = min(newarray[:,0]), min(newarray[:,1]) # Get min lat and lon to subtract from pts
cart_array = 100*(newarray[0::50,0:2] - [min_lat, min_lon]) # Scaling by 100 and sampling by every 50 to spread out the data
sampled_pop = newarray[0::50]

# Define the beacon locations (randomly located in the unit square)
# x_beac=[0.7984,0.9430,0.6837,0.1321,0.7227,0.1104,0.1175,0.6407,0.3288,0.6538]
# y_beac=[0.7491,0.5832,0.7400,0.2348,0.7350,0.9706,0.8669,0.0862,0.3664,0.3692]
x_beac = cart_array[:,1] # Swapping order for plotting purposes
y_beac = cart_array[:,0]

# Generate the (noisy) data y, and set initial guess
noise_level=0.05
y=np.zeros(len(x_beac))
for i in range(len(x_beac)):
    dx=bx_t-x_beac[i]
    dy=by_t-y_beac[i]
    y[i]=sqrt(dx*dx+dy*dy)+noise_level*random()
b_init=np.array([150.,135.]) #=np.array(0.4,0.9)

# Function to be minimized
def phi(x):
    s=0
    for i in range(len(x_beac)):
        dx=x[0]-x_beac[i]
        dy=x[1]-y_beac[i]
        ss=sqrt(dx*dx+dy*dy)-y[i]
        s+=ss*ss
    return s

# Gradient
def grad_phi(x):
    f0=0
    f1=0
    for i in range(len(x_beac)):
        dx=x[0]-x_beac[i]
        dy=x[1]-y_beac[i]
        d=1/sqrt(dx*dx+dy*dy)
        f0+=2*dx-2*y[i]*dx*d
        f1+=2*dy-2*y[i]*dy*d
    return np.array([f0,f1])

# Do Levenberg-Marquardt algorithm and print diagnostic information
sol=root(grad_phi,b_init,jac=False,method='lm')
print "Predicted location:",sol.x
print "grad(phi):",grad_phi(sol.x)
print "phi:",phi(sol.x)

# Plot results
n=100
xx=np.linspace(0,1,n)
yy=np.linspace(0,1,n)
X,Y=np.meshgrid(xx,yy)
pxy=np.zeros((n,n))
for i in range(n):
    for j in range(n):
        pxy[i,j]=phi([X[i,j],Y[i,j]])
plt.contourf(X, Y, pxy, 16, alpha=.75)
C = plt.contour(X, Y, pxy, 16, colors='black', linewidth=.5)
plt.plot(x_beac,y_beac,'o',alpha=0.7)
plt.plot(sol.x[0],sol.x[1],'*', lw=4, markersize=15, color='red')
plt.plot(b_init[0],b_init[1],'o', markersize=15, color='black')
plt.show()
