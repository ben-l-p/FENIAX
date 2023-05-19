import numpy as np 

######################
# FEM Files Settings #
######################
op2name=''
M_a='/media/pcloud/Computations/FEM4INAS/Models/GolandWinglong/FEM/Maa.npy'
q0_file=''
model_name='/Models/GolandWinglong'
Grid='/media/pcloud/Computations/FEM4INAS/Models/GolandWinglong/FEM/structuralGrid'
K_a='/media/pcloud/Computations/FEM4INAS/Models/GolandWinglong/FEM/Kaa.npy'
model='GolandWinglong'
feminas_dir='/media/pcloud/Computations/FEM4INAS'
###########################
# Read Grid File Settings #
###########################
start_reading=3
node_start=1
nodeorder_start=0
beam_start=0
#####################
# Topology Settings #
#####################
Nastran_modes=0
Path4Phi2=0
ReplaceRBmodes=0
NumBeams=1
NumModes_res=0
NumModes=12
BeamConn=[[[]], [[]]]
Check_Phi2=0
#################
# Time Settings #
#################
t0=0.0
tn=20000
ti=np.linspace(0.0,40.0,20000)
tf=40.0
dt=0.002000100005
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
MBnode={}
MBbeams=[]
ClampX=np.array([2.,0.,0.166667])
BeamsClamped=[0]
RigidBody_Modes=0
MBdofree={}
MBdof={}
MBnode2={}
initialbeams=[0]
Clamped=1
####################
# Loading Settings #
####################
loading=1
linear=0
dynamic=1
static=0
init_q0=None
