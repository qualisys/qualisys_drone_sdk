import asyncio
import contextlib
import math
import os
import random
import pynput
from time import sleep, time

from qfly import Pose, QualisysCrazyflie, World, utils, parallel

import numpy as np

# SETTINGS
# QTM rigid body names
cf_body_names = [
    'E7E7E7E701',
    'E7E7E7E702',
    # 'E7E7E7E703'
]
# Crazyflie addresses
cf_uris = [
    'radio://0/80/1M/E7E7E7E701',
    'radio://0/80/1M/E7E7E7E702',
    # 'radio://0/80/1M/E7E7E7E703'
]

# Crazyflie addresses
cf_marker_ids = [
    [11, 12, 13, 14],
    [21, 22, 23, 24],
    # [31, 32, 33, 34]
]

# Watch key presses with a global variable
last_key_pressed = None


# Set up keyboard callback
def on_press(key):
    """React to keyboard."""
    global last_key_pressed
    last_key_pressed = key
    if key == pynput.keyboard.Key.esc:
        os.exit(1)


# Listen to the keyboard
listener = pynput.keyboard.Listener(on_press=on_press)
listener.start()


# Set up world - the World object comes with sane defaults
world = World()

# Stack up context managers

_qcfs = [QualisysCrazyflie(cf_body_name,
                           cf_uri,
                           world,
                           marker_ids=cf_marker_id)
         for cf_body_name, cf_uri, cf_marker_id
         in zip(cf_body_names, cf_uris, cf_marker_ids)]

with parallel(*_qcfs) as qcfs:

    # Let there be time
    t = time()
    dt = 0

    print("Beginning maneuvers...")

    # MAIN LOOP WITH SAFETY CHECK
    while(dt < 32):

        # Land with L key
        if hasattr(last_key_pressed, 'char'):
            if last_key_pressed.char == "l":
                break

        # Mind the clock
        dt = time() - t

        for idx, qcf in enumerate(qcfs):

            # Take off and hover in the center of safe airspace
            if dt < 5:
                print(f'[t={int(dt)}] Liftoff...')
                qcf.ascend()

            elif t < 8:
                print(f'[t={int(dt)}] Maneuvering - Center...')
                # Set target
                x = np.interp(idx,
                              [0,
                               len(qcfs) - 1],
                              [world.origin.x - world.expanse / 2,
                               world.origin.x + world.expanse / 2])
                target = Pose(x,
                              world.origin.y,
                              world.expanse)
                # Engage
                qcf.safe_position_setpoint(target)
                sleep(0.1)

            # Make sphere
            elif dt < 28:
                print(f'[t={int(dt)}] Maneuvering - Sphere...')
                # Set target
                # Calculate angles based on time
                phi = (dt * 180) % 360
                # theta = (math.sin((dt * 60) % 180) + 1) * 90
                theta = 90
                # Offset angle based on array
                phi = (phi + (360 / len(qcfs)) * (idx / len(qcfs))) % 360
                # theta = (theta + (180 / len(qcfs)) * (idx / len(qcfs))) % 180
                _x, _y, _z = utils.sph2cart(0.5, theta, phi)
                target = Pose(world.origin.x + _x,
                              world.origin.y + _y,
                              world.expanse + _z)
                print("TARGET ANGLE FOR " + str(idx) + " => " + str(phi))
                # Engage
                qcf.safe_position_setpoint(target)
                sleep(0.1)

            # Back to center
            elif dt < 32:
                print(f'[t={int(dt)}] Maneuvering - Center...')
                # Set target
                x = np.interp(idx,
                              [0,
                               len(qcfs) - 1],
                              [world.origin.x - world.expanse / 2,
                               world.origin.x + world.expanse / 2])
                target = Pose(x,
                              world.origin.y,
                              world.expanse)
                # Engage
                qcf.safe_position_setpoint(target)
                sleep(0.1)

    # Land calmly
    while(any(qcf.pose.z > 0.1 for qcf in qcfs)):
        for qcf in qcfs:
            qcf.descend()
