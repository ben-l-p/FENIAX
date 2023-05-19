Dead_interpol=None #Interpolation of the dead forces [ [ [[t0,t1...tn],[f0,f1...fn]]..Coordinates..]..NumFLoads..]
Follower_points_app=[[0, -1, [0, 1, 2]]] #Points of the applied follower loads [[BeamSeg,Node,[..Coordinates..]]..NumFLoads..]
NumDLoads=0 #Number of (point) dead forces
Dead_points_app=None #Points of the applied dead loads [[BeamSeg,Node,[..Coordinates..]]..NumFLoads..]
Gravity=0 #Gravity loads
NumFLoads=1 #Number of (point) follower forces 
NumALoads=1 #0 or 1 for including aerodynamic forces
Follower_interpol=[[[[0.0, 12.0, 13.0, 14.0, 30.0, 31, 32.0, 50.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]], [[0.0, 12.0, 13.0, 14.0, 30.0, 31, 32.0, 50.0], [0.0, 0.0, 20.0, 0.0, 0.0, -20.0, 0.0, 0.0]], [[0.0, 12.0, 13.0, 14.0, 30.0, 31, 32.0, 50.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]]] #Interpolation of the follower forces [ [ [[t0,t1...tn],[f0,f1...fn]]..Coordinates..]..NumFLoads..]
