import numpy as np 

######################
# FEM Files Settings #
######################
op2name=''
M_a='/home/ac5015/Dropbox/Computations/FEM4INAS/Models/Hesse_25n/FEM/Maa.npy'
q0_file=''
model_name='/Models/Hesse_25n'
Grid='/home/ac5015/Dropbox/Computations/FEM4INAS/Models/Hesse_25n/FEM/structuralGrid'
K_a='/home/ac5015/Dropbox/Computations/FEM4INAS/Models/Hesse_25n/FEM/Kaa.npy'
model='Hesse_25n'
feminas_dir='/home/ac5015/Dropbox/Computations/FEM4INAS'
###########################
# Read Grid File Settings #
###########################
start_reading=3
node_start=1
nodeorder_start=0
beam_start=1
#####################
# Topology Settings #
#####################
Nastran_modes=0
NumBeams=1
NumModes_res=0
NumModes=112
BeamConn=[[[]], [[]]]
Check_Phi2=0
#################
# Time Settings #
#################
t0=0.0
tn=2872
ti=np.linspace(0.0,10.0,2872)
tf=10.0
dt=0.00348310693138
######################
# Constants Settings #
######################
I3=np.eye(3)
e_1=np.array([1.,0.,0.])
EMAT=np.array([[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,-1,0,0,0],[0,1,0,0,0,0]])
g=9.80665
#####################
# Boundary Settings #
#####################
ClampX=[]
BeamsClamped=[]
RigidBody_Modes=1
Clamped=0
####################
# Loading Settings #
####################
loading=1
linear=0
dynamic=1
static=0
init_q0=None
