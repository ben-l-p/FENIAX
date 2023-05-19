import numpy as np
import os
from wing_inp import *
#import pyNastran
for i in range(len(os.getcwd().split('/'))):
  if os.getcwd().split('/')[-i-1]=='FEM4INAS':
    feminas_dir="/".join(os.getcwd().split('/')[0:-i])

model='wingA380_30'

sol='400'
static = 0
dynamic = 1
rotation=0
#Loads
FORCE1=1
numLoads=1
numForce=1
Fl=[[150.]]
Ml=None
Fd=[[[0.,0.,1.]] for i in range(numLoads)]
#Md=[[[0.,-1.,0.]] for i in range(numLoads)]
gridF=[[500030] for i in range(numLoads)]

Acceleration0 = 0
Velocity0 = 0
Displacement0 = 0

ug=range(na)
vg=range(na)
ag=range(na)

def fv(x):
  return 1.5*np.array(0.,1.,1.)

def fu(x):
  return 2*x

def fu(x):
  return 2*x

#ti=2000.
tableti=[[[0.,0.],[4.,1.],[4.,0.],[25.,0.]]]
ti_max = 20.
ti_n = 4000
