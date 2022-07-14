
"""
qfly | Qualisys Drone SDK Example Script: Interactive Crazyflie with Traqr

Drones take off and fly circles around Z axis.

The altitude (z) tracks a Traqr or other appropriately configured
rigid body.
ESC to land at any time.
"""

import pynput
from time import sleep, time

from qfly import Pose, QualisysCrazyflie, QualisysTraqr, World, parallel_contexts, utils

import numpy as np

# SETTINGS
# QTM rigid body names
cf_body_names = [
    'E7E7E7E701',
    'E7E7E7E702',
    # 'E7E7E7E703',
    # 'E7E7E7E704',
]
# Crazyflie addresses
cf_uris = [
    'radio://0/80/2M/E7E7E7E701',
    'radio://0/80/2M/E7E7E7E702',
    # 'radio://0/80/2M/E7E7E7E703',
    # 'radio://0/80/2M/E7E7E7E704',
]

# Crazyflie addresses
cf_marker_ids = [
    [11, 12, 13, 14],
    [21, 22, 23, 24],
    # [31, 32, 33, 34],
    # [41, 42, 43, 44],
]

# Traqr
traqr_body_name = "10261"
    

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
world = World(expanse=1)

# Stack up context managers
_qcfs = [QualisysCrazyflie(cf_body_name,
                           cf_uri,
                           world,
                           marker_ids=cf_marker_id)
         for cf_body_name, cf_uri, cf_marker_id
         in zip(cf_body_names, cf_uris, cf_marker_ids)]

with QualisysTraqr(traqr_body_name) as traqr:
    with parallel_contexts(*_qcfs) as qcfs:

        # Let there be time
        t = time()
        dt = 0

        print("Beginning maneuvers...")

        # MAIN LOOP WITH SAFETY CHECK
        while(all(qcf.is_safe() for qcf in qcfs)):

            # Land with Esc
            if last_key_pressed == pynput.keyboard.Key.esc:
                break

            # Mind the clock
            dt = time() - t

            # Track the Traqr
            if traqr.pose is not None:
                z = traqr.pose.z
                # Clip bottom and don't crash drones on the floor
                if z < 0.4:
                    z = 0.4
            else:
                z = world.expanse

            for idx, qcf in enumerate(qcfs):

                # Take off and hover in the center of safe airspace
                if dt < 5:
                    qcf.set_led_ring(1)
                    print(f'[t={int(dt)}] Maneuvering - Center...')
                    # Set target
                    x = np.interp(idx,
                                  [0,
                                   len(qcfs) - 1],
                                  [world.origin.x - world.expanse * 0.8,
                                   world.origin.x + world.expanse * 0.8])
                    target = Pose(x,
                                  world.origin.y,
                                  world.expanse)
                    # Engage
                    qcf.safe_position_setpoint(target)

                    sleep(0.1)

                # Move out half of the safe airspace in the X direction and circle around Z axis
                else:
                    print(f'[t={int(dt)}] Maneuvering - Circle around Z...')
                    # Set target
                    phi = (dt * 90) % 360  # Calculate angle based on time
                    # Offset angle based on array
                    phi = phi + 360 * (idx / len(qcfs))
                    _x, _y = utils.pol2cart(0.75, phi)
                    target = Pose(world.origin.x + _x,
                                  world.origin.y + _y,
                                  z)
                    print("TARGET ANGLE FOR " + str(idx) + " => " + str(phi))
                    # Engage
                    qcf.safe_position_setpoint(target)
                    sleep(0.02)

        # Land calmly
        while(any(qcf.pose.z > 0.1 for qcf in qcfs)):
            for qcf in qcfs:
                qcf.descend()
