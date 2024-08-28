import time
import os
import signal
import numpy as np
from nicomotors import NicoMotors
import matplotlib.pyplot as plt

JOINT = 'right-elbow1'
STARTSPEED = 100
ENDSPEED = 1000
STEPSPEED = 10
CONSTANTSPEED = (np.mean([STARTSPEED,ENDSPEED])/2)
CONSTANTSPEED = STARTSPEED
SLEEP = 0.05
REPETITION = 10

motors = NicoMotors()
dofs = motors.dofs()
try:
    motors.open()
except:
    print('motors are not operational')
time.sleep(0.5)
STARTPOS = motors.getRange(JOINT)[0]
ENDPOS = motors.getRange(JOINT)[1]

var_positions = []
const_positions = []
var_diffs = []
const_diffs = []



for r in range(REPETITION):
    
    # Variable speed
    diffs = []
    positions = []
    steps = []
    motors.setMovingSpeed(JOINT, STARTSPEED)
    motors.setPosition(JOINT, STARTPOS)
    time.sleep(2)
    last = motors.getPosition(JOINT)
    
    for i in range(STARTSPEED, ENDSPEED, STEPSPEED):
        speed = i
        motors.setMovingSpeed(JOINT, speed)
        motors.setPosition(JOINT, ENDPOS)
        time.sleep(SLEEP)
        actual = motors.getPosition(JOINT)
        actualspeed = motors.getMovingSpeed(JOINT)
        diff = actual - last
        print(f'Speed: {speed}, Position: {actual}, Diff: {diff}, Actual Speed: {actualspeed}')
        diffs.append(diff)
        positions.append(actual)
        steps.append(i)
        last = actual


    var_positions.append(positions)
    var_diffs.append(diffs)

    print (f'Variable speed trial #{r}')
    # Constant speed
    diffs = []
    positions = []
    steps = []
    motors.setMovingSpeed(JOINT, STARTSPEED)
    motors.setPosition(JOINT, STARTPOS)
    time.sleep(2)
    last = motors.getPosition(JOINT)

    speed = int(CONSTANTSPEED)
    motors.setMovingSpeed(JOINT, speed)
    motors.setPosition(JOINT, ENDPOS)

    for i in range(STARTSPEED, ENDSPEED, STEPSPEED):
        
        time.sleep(SLEEP)
        actual = motors.getPosition(JOINT)
        actualspeed = motors.getMovingSpeed(JOINT)
        diff = actual - last
        print(f'Speed: {speed}, Position: {actual}, Diff: {diff}, Actual Speed: {actualspeed}')
        diffs.append(diff)
        positions.append(actual)
        steps.append(i)
        last = actual
    
    const_positions.append(positions)
    const_diffs.append(diffs)

    print (f'Constant speed trial #{r}')
var_positions = np.array(var_positions)
var_diffs = np.array(var_diffs)
const_positions = np.array(const_positions)
const_diffs = np.array(const_diffs)


# Calculate average and standard deviation
avg_var_positions = np.mean(var_positions, axis=0)
std_var_positions = np.std(var_positions, axis=0)
avg_const_positions = np.mean(const_positions, axis=0)
std_const_positions = np.std(const_positions, axis=0)

avg_var_diffs = np.mean(var_diffs, axis=0)
std_var_diffs = np.std(var_diffs, axis=0)
avg_const_diffs = np.mean(const_diffs, axis=0)
std_const_diffs = np.std(const_diffs, axis=0)

# Plotting the values
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))


    
fig.suptitle(f'Joint: {JOINT}, Constant speed: {CONSTANTSPEED}, Variable speed {STARTSPEED} - {ENDSPEED})', fontsize=16)

ax1.plot(steps, avg_const_positions, color='tab:blue', label='Constant Speed')
ax1.fill_between(steps, avg_const_positions - std_const_positions, avg_const_positions + std_const_positions, color='tab:blue', alpha=0.2)
ax1.plot(steps,avg_var_positions, color='tab:red', label='Variable Speed')
ax1.fill_between(steps, avg_var_positions - std_var_positions, avg_var_positions + std_var_positions, color='tab:red', alpha=0.2)
ax1.set_title('Actual Position')
ax1.set_ylabel('Position')
ax1.set_xlabel('Blue Steps/Red Speed')
ax1.legend()

ax2.plot(steps, avg_const_diffs, color='tab:blue', label='Constant Speed' )
ax2.fill_between(steps, avg_const_diffs - std_const_diffs, avg_const_diffs + std_const_diffs, color='tab:blue', alpha=0.2)
ax2.plot(steps,avg_var_diffs, color='tab:red', label='Variable Speed')
ax2.fill_between(steps, avg_var_diffs - std_var_diffs, avg_var_diffs + std_var_diffs, color='tab:red', alpha=0.2)
ax2.set_title('Last-Actual Pos Difference')
ax2.set_ylabel('Position')
ax2.set_xlabel('Blue Steps/Red Speed')
ax2.legend()

fig.tight_layout()
fig.savefig(f'{JOINT}_{STARTSPEED}_{CONSTANTSPEED}_{ENDSPEED}_UKBA.png')




motors.setMovingSpeed(JOINT, STARTSPEED)
motors.setPosition(JOINT,STARTPOS)
plt.show()


