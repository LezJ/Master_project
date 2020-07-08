import time
import sim
import sys
import math
import random
import copy


# Set the arm to its initial status
def ini_state():
    for i in range(3):
        sim.simxSetJointTargetVelocity(clientID, jointHandles[i][1], -closingVel, sim.simx_opmode_streaming)
        sim.simxSetJointTargetVelocity(clientID, jointHandles[i][2], -closingVel/3, sim.simx_opmode_streaming)
    # sim.simxSetJointTargetPosition(clientID, jointHandles[0][0], -math.pi*0.5, sim.simx_opmode_streaming)
    # sim.simxSetJointTargetPosition(clientID, jointHandles[2][0], -math.pi*0.5, sim.simx_opmode_streaming)
    
    sim.simxSetJointTargetPosition(clientID, j4, -math.pi*0.5, sim.simx_opmode_streaming)
    sim.simxSetJointTargetPosition(clientID, j6, math.pi*0.5, sim.simx_opmode_streaming)

# Set the object to its initial position and orientation
def ob_ini_state(o_ini, p_ini):
    o = copy.deepcopy(o_ini)
    p = copy.deepcopy(p_ini)
    sim.simxSetObjectOrientation(clientID, ob_handle, -1, o, sim.simx_opmode_oneshot)
    sim.simxSetObjectPosition(clientID, ob_handle, -1, p, sim.simx_opmode_oneshot)
    
# Read one set of sensors' data and note them down
def sensors_read(doc):
    for i in range(3):
        
        returnCode, state, forceVector, torqueVector = sim.simxReadForceSensor(clientID, fingerTipSensor[i], sim.simx_opmode_buffer)
        print('TS' + str(i) , forceVector, file = doc)

        returnCode, state, forceVector1, torqueVector = sim.simxReadForceSensor(clientID, FS[i], sim.simx_opmode_buffer)
        print('FS' + str(i) , forceVector1, file = doc)
        
        returnCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.simxReadProximitySensor(clientID, PS[i], sim.simx_opmode_buffer)
        print('PS' + str(i) , detectedPoint, file = doc)
        
    returnCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.simxReadProximitySensor(clientID, PS[3], sim.simx_opmode_buffer)
    print('PS3', detectedPoint, file = doc)
        
        
# Define the closing and opening movement for different grasp modes
def g_mode(g_type, status):
    
    if g_type == '2A1':
        sim.simxSetJointTargetPosition(clientID, jointHandles[0][0], -math.pi*0.5, sim.simx_opmode_streaming)
        sim.simxSetJointTargetPosition(clientID, jointHandles[2][0], -math.pi*0.5, sim.simx_opmode_streaming)
        
        if status == 'closing':
            for i in range(3):
                sim.simxSetJointTargetVelocity(clientID, jointHandles[i][1], closingVel, sim.simx_opmode_streaming)
        
        else:
            for i in range(3):
                sim.simxSetJointTargetVelocity(clientID, jointHandles[i][1], openingVel, sim.simx_opmode_streaming)
    
    if g_type == 'Wide':
        sim.simxSetJointTargetPosition(clientID, jointHandles[0][0], -math.pi*1/4, sim.simx_opmode_streaming)
        sim.simxSetJointTargetPosition(clientID, jointHandles[2][0], -math.pi*1/4, sim.simx_opmode_streaming)
        
        if status == 'closing':
            for i in range(3):
                sim.simxSetJointTargetVelocity(clientID, jointHandles[i][1], closingVel, sim.simx_opmode_streaming)
        
        else:
            for i in range(3):
                sim.simxSetJointTargetVelocity(clientID, jointHandles[i][1], openingVel, sim.simx_opmode_streaming)    
                
    # if g_type == 'Scissor':
    #     sim.simxSetJointTargetPosition(clientID, jointHandles[0][0], -math.pi*0.5, sim.simx_opmode_streaming)
    #     sim.simxSetJointTargetPosition(clientID, jointHandles[2][0], -math.pi*0.5, sim.simx_opmode_streaming)
        
    #     if status == 'closing':
    #         sim.simxSetJointTargetVelocity(clientID, jointHandles[0][1], closingVel, sim.simx_opmode_streaming)
    #         sim.simxSetJointTargetVelocity(clientID, jointHandles[2][1], closingVel, sim.simx_opmode_streaming)
        
    #     else:
    #         sim.simxSetJointTargetVelocity(clientID, jointHandles[0][1], openingVel, sim.simx_opmode_streaming)
    #         sim.simxSetJointTargetVelocity(clientID, jointHandles[2][1], openingVel, sim.simx_opmode_streaming)


# One grasp in a single mode, read the data during the grasp(100Hz)
def one(g_type, doc):
    g_mode(g_type,'open')
    time.sleep(1)
    # for i in range(10):
    #     returnCode, state, forceVector, torqueVector = sim.simxReadForceSensor(clientID, fs1, sim.simx_opmode_buffer)
    #     print(forceVector)
    #     time.sleep(0.1)
        
    g_mode(g_type,'closing')
    # time.sleep(1)
    for i in range(150):
        sensors_read(doc)
        time.sleep(0.01)
    sim.simxSetJointTargetPosition(clientID, j4, -1, sim.simx_opmode_streaming)
#    time.sleep(1)
    sim.simxSetJointTargetPosition(clientID, j6, 1, sim.simx_opmode_streaming)
    # time.sleep(1)
    for i in range(100):
        sensors_read(doc)
        time.sleep(0.01)
    g_mode(g_type,'open')
    for i in range(50):
        sensors_read(doc)
        time.sleep(0.01)
    
# Randomly change the position(+-0.01m) and orientation of the object
def ob_re_altering(o_ini, p_ini):
    o = copy.deepcopy(o_ini)
    p = copy.deepcopy(p_ini)
    sim.simxSetObjectOrientation(clientID, ob_handle, -1, o, sim.simx_opmode_oneshot)
    sim.simxSetObjectPosition(clientID, ob_handle, -1, p, sim.simx_opmode_oneshot)
    time.sleep(0.5)
    
    o_delta = random.uniform(0, math.pi*0.5)
    o[2] += o_delta
    sim.simxSetObjectOrientation(clientID, ob_handle, -1, o, sim.simx_opmode_oneshot)
    
    x_p_delta = random.uniform(-0.01, 0.01)
    y_p_delta = random.uniform(-0.01, 0.01)
    p[0] += x_p_delta
    p[1] += y_p_delta
    sim.simxSetObjectPosition(clientID, ob_handle, -1, p, sim.simx_opmode_oneshot)
    
# Start a simulation, by giving the grasp mode and number of times
def start_simulation(g_type, times):
    
    doc = open('D:\Py\Vrep\Data\data_ww_0.txt','w')
    ob_ini_state(ob_o, ob_p)
    for i in range(times):

        print('Grasp', i+1 , file = doc)
        print('Grasp', i+1, 'handling')
        one(g_type, doc)
        time.sleep(1)
        ob_re_altering(ob_o, ob_p)
        time.sleep(0.5)
        ini_state()
        time.sleep(0.5)
        
    doc.close()
        


sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
if clientID!=-1:
    print ('Connected to remote API server')
    sim.simxSynchronous(clientID,True)
    res,objs=sim.simxGetObjects(clientID,sim.sim_handle_all,sim.simx_opmode_blocking)
    if res==sim.simx_return_ok:
	    print('Number of objects in the scene: ',len(objs))
else:
    print('Fail to connect')
    sys.exit()
    
# Set the target object
ob = 'Cuboid' 

# Initializate the system. Handle and properly set the needed joints and sensors

jointHandles = [[-1,-1,-1], [-1,-1,-1], [-1,-1,-1]]
firstPartTorqueSensorHandles = [-1,-1,-1]
closingVel=60*math.pi/180
openingVel=-120*math.pi/180
closingOpeningTorque=1

ob_handle = sim.simxGetObjectHandle(clientID, ob, sim.simx_opmode_blocking)[1]
ob_p = sim.simxGetObjectPosition(clientID, ob_handle, -1, sim.simx_opmode_streaming)[1]
ob_o = sim.simxGetObjectOrientation(clientID, ob_handle, -1, sim.simx_opmode_streaming)[1]

# Handle needed joints of the arm and note down their initial positions
j4 = sim.simxGetObjectHandle(clientID, 'Franka_joint4', sim.simx_opmode_blocking)[1]
j6 = sim.simxGetObjectHandle(clientID, 'Franka_joint6', sim.simx_opmode_blocking)[1]

ob_p = sim.simxGetObjectPosition(clientID, ob_handle, -1, sim.simx_opmode_streaming)[1]
ob_o = sim.simxGetObjectOrientation(clientID, ob_handle, -1, sim.simx_opmode_streaming)[1]

# Handle and properly set the needed joints of the hand
for i in range(3):
    if i != 1:
        jointHandles[i][0] = sim.simxGetObjectHandle(clientID, 'BarrettHand_jointA_' + str(i), sim.simx_opmode_blocking)[1]
    jointHandles[i][1] = sim.simxGetObjectHandle(clientID, 'BarrettHand_jointB_' + str(i), sim.simx_opmode_blocking)[1]
    jointHandles[i][2] = sim.simxGetObjectHandle(clientID, 'BarrettHand_jointC_' + str(i), sim.simx_opmode_blocking)[1]
 
for i in range(3):
    sim.simxSetObjectIntParameter(clientID, jointHandles[i][1], sim.sim_jointintparam_motor_enabled, 1, sim.simx_opmode_oneshot)
    sim.simxSetObjectIntParameter(clientID, jointHandles[i][1], sim.sim_jointintparam_ctrl_enabled, 0, sim.simx_opmode_oneshot)
    sim.simxSetObjectIntParameter(clientID, jointHandles[i][2], sim.sim_jointintparam_motor_enabled, 1, sim.simx_opmode_oneshot)
    sim.simxSetObjectIntParameter(clientID, jointHandles[i][2], sim.sim_jointintparam_ctrl_enabled, 1, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, jointHandles[i][1], -closingVel, sim.simx_opmode_streaming)
    sim.simxSetJointTargetVelocity(clientID, jointHandles[i][2], -closingVel/3, sim.simx_opmode_streaming)
    sim.simxSetJointForce(clientID,jointHandles[i][1], closingOpeningTorque, sim.simx_opmode_oneshot)
    sim.simxSetJointForce(clientID,jointHandles[i][2], closingOpeningTorque, sim.simx_opmode_oneshot)


sim.simxSetJointTargetPosition(clientID, jointHandles[0][0], -math.pi*0.5, sim.simx_opmode_streaming)
sim.simxSetJointTargetPosition(clientID, jointHandles[2][0], -math.pi*0.5, sim.simx_opmode_streaming)

# time.sleep(1)

# ob_handle = sim.simxGetObjectHandle(clientID, ob, sim.simx_opmode_blocking)[1]
# ob_p = sim.simxGetObjectPosition(clientID, ob_handle, -1, sim.simx_opmode_streaming)[1]
# ob_o = sim.simxGetObjectOrientation(clientID, ob_handle, -1, sim.simx_opmode_streaming)[1]

# # Handle needed joints of the arm and note down their initial positions
# j4 = sim.simxGetObjectHandle(clientID, 'Franka_joint4', sim.simx_opmode_blocking)[1]
# j6 = sim.simxGetObjectHandle(clientID, 'Franka_joint6', sim.simx_opmode_blocking)[1]

# ob_p = sim.simxGetObjectPosition(clientID, ob_handle, -1, sim.simx_opmode_streaming)[1]
# ob_o = sim.simxGetObjectOrientation(clientID, ob_handle, -1, sim.simx_opmode_streaming)[1]
time.sleep(0.5)

fingerTipSensor = [0,0,0]
FS = [0,0,0]
PS = [0,0,0,0]

# Handle the sensors and prepare them to be read
for i in range(3):
    fingerTipSensor[i] = sim.simxGetObjectHandle(clientID, 'BarrettHand_fingerTipSensor' + str(i), sim.simx_opmode_blocking)[1]
    print(sim.simxReadForceSensor(clientID, fingerTipSensor[i], sim.simx_opmode_streaming))
    FS[i] = sim.simxGetObjectHandle(clientID, 'FS' + str(i), sim.simx_opmode_blocking)[1]
    print(sim.simxReadForceSensor(clientID, FS[i], sim.simx_opmode_streaming))
    PS[i] = sim.simxGetObjectHandle(clientID, 'PS' + str(i), sim.simx_opmode_blocking)[1]
    print(sim.simxReadProximitySensor(clientID, PS[i], sim.simx_opmode_streaming))
    
PS[3] = sim.simxGetObjectHandle(clientID, 'PS3', sim.simx_opmode_blocking)[1]
sim.simxReadProximitySensor(clientID, PS[3], sim.simx_opmode_streaming)    



