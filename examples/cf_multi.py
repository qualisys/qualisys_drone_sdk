"""
qfly | Qualisys Drone SDK Example Script: Multi Crazyflie

Drones take off and fly circles around Z axis.
ESC to land at any time.
"""


import pynput
from time import sleep, time

from qfly import Pose, QualisysCrazyflie, World, ParallelContexts, utils

import numpy as np

# SETTINGS
# QTM rigid body names
cf_body_names = [
    'Crazyflie1',
    'Crazyflie2'
]
# Crazyflie addresses
cf_uris = [
    'radio://0/80/2M/E7E7E7E701',
    'radio://0/80/2M/E7E7E7E702'
]
# Crazyflie marker ids
cf_marker_ids = [
    [11, 12, 13, 14],
    [21, 22, 23, 24]
]


# Watch key presses with a global variable
last_key_pressed = None


# Set up keyboard callback
def on_press(key):
    """React to keyboard."""
    global last_key_pressed
    last_key_pressed = key


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

with ParallelContexts(*_qcfs) as qcfs:

    # Let there be time
    t = time()
    dt = 0

    print("Beginning maneuvers...")

    # "fly" variable used for landing on demand
    fly = True

    # MAIN LOOP WITH SAFETY CHECK
    while(fly and all(qcf.is_safe() for qcf in qcfs)):

        # Land with Esc
        if last_key_pressed == pynput.keyboard.Key.esc:
            break

        # Mind the clock
        dt = time() - t

        # Cycle all drones
        for idx, qcf in enumerate(qcfs):

            # Take off and hover in the center of safe airspace
            if dt < 3:
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
                sleep(0.02)

            # Move out half of the safe airspace in the X direction and circle around Z axis
            elif dt < 30:
                print(f'[t={int(dt)}] Maneuvering - Circle around Z...')
                # Set target
                phi = (dt * 90) % 360  # Calculate angle based on time
                # Offset angle based on array
                phi = phi + 360 * (idx / len(qcfs))
                _x, _y = utils.pol2cart(0.5, phi)
                target = Pose(world.origin.x + _x,
                              world.origin.y + _y,
                              world.expanse)
                # Engage
                qcf.safe_position_setpoint(target)
                sleep(0.02)

            # Back to center
            elif dt < 33:
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
                sleep(0.02)

            else:
                fly = False

     # Land
    while (qcf.pose.z > 0.1):
        for idx, qcf in enumerate(qcfs):
            qcf.land_in_place()
            sleep(0.02)
