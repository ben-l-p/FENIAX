import numpy as np 

Grid='/home/ac5015/Dropbox/Computations/FEM4INAS/Models/RafaBeam_200/FEM/structuralGrid'
K_a='/home/ac5015/Dropbox/Computations/FEM4INAS/Models/RafaBeam_200/FEM/Kaa.npy'
M_a='/home/ac5015/Dropbox/Computations/FEM4INAS/Models/RafaBeam_200/FEM/Maa.npy'
op2name=''
feminas_dir='/home/ac5015/Dropbox/Computations/FEM4INAS'
model_name='/Models/RafaBeam_200'
model='RafaBeam_200'
q0_file='q0_002.npy'
node_start=1
start_reading=3
beam_start=1
nodeorder_start=1
NumModes=1200
NumBeams=1
BeamConn=[[[]], [[]]]
Nastran_modes=0
loading=0
static=0
dynamic=1
init_q0=1
linear=1
t0=0
tf=20
tn=10000
dt=0.00200020002
RigidBody_Modes=0
Clamped=1
ClampX=np.array([0.,0.,0.])
BeamsClamped=[0]
EMAT=np.array([[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,-1,0,0,0],[0,1,0,0,0,0]])
I3=np.eye(3)
e_1=np.array([1,0,0])
