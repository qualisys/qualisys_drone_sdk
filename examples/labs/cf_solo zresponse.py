"""
qfly | Qualisys Drone SDK Example Script: Control Engineering / Step Response Demo

EXPERIMENTAL
"""

import pynput
from time import sleep, time

import numpy as np
import matplotlib.pyplot as plt

from qfly import Pose, QualisysCrazyflie, World


# SETTINGS
cf_body_name = 'E7E7E7E704'  # QTM rigid body name
cf_uri = 'radio://0/80/2M/E7E7E7E704'  # Crazyflie address
cf_marker_ids = [41, 42, 43, 44]


# Watch key presses with a global variable
last_key_pressed = None


# Set up keyboard callback
def on_press(key):
    """React to keyboard."""
    global last_key_pressed
    last_key_pressed = key
    if key == pynput.keyboard.Key.esc:
        fly = False


# Listen to the keyboard
listener = pynput.keyboard.Listener(on_press=on_press)
listener.start()


# Set up world - the World object comes with sane defaults
world = World()


# Prepare for liftoff
with QualisysCrazyflie(cf_body_name,
                       cf_uri,
                       world,
                       marker_ids=cf_marker_ids) as qcf:

    # Let there be time
    t = time()
    dt = 0

    print("Beginning maneuvers...")

    log = []

    # MAIN LOOP WITH SAFETY CHECK
    while(qcf.is_safe()):

        # Terminate upon Esc command
        if last_key_pressed == pynput.keyboard.Key.esc:
            break

        # Mind the clock
        dt = time() - t

        # Keep track of altitude
        log.append(qcf.pose)

        # Take off and hover in the center of safe airspace for 5 seconds
        if dt < 20:
            print(f'[t={int(dt)}] Ascending...')
            qcf.rise_in_place()
            continue

        if dt < 30:
            qcf.land_in_place()
            continue

        # if dt < 50:
        #     print(f'[t={int(dt)}] Ascending...')
        #     qcf.rise_in_place(0.7)
        #     continue

        # if dt < 60:
        #     qcf.land_in_place()
        #     continue
        
        # if dt < 80:
        #     print(f'[t={int(dt)}] Ascending...')
        #     qcf.rise_in_place(0.4)
        #     continue

        # if dt < 90:
        #     qcf.land_in_place()
        #     continue

        else:
            break

    # Land calmly
    qcf.land_in_place()

# Plot z-axis response
_t = range(len(log))
_x = list(pose.x for pose in log)
_y = list(pose.y for pose in log)
_z = list(pose.z for pose in log)
fig, ax = plt.subplots()
ax.scatter(_x, _y)


plt.show()
