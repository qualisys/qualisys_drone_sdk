import contextlib
import random
import pynput
from time import sleep, time

from qfly import Pose, QualisysCrazyflie, World, utils

import numpy as np

# SETTINGS
# QTM rigid body names
cf_body_names = ['E7E7E7E701',
                 'E7E7E7E702']
# Crazyflie addresses
cf_uris = ['radio://0/80/1M/E7E7E7E701',
           'radio://0/80/1M/E7E7E7E702']

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

# Stack up context managers
with contextlib.ExitStack() as stack:
    # Init drones
    qcfs = [
        stack.enter_context(QualisysCrazyflie(
            cf_body_name,
            cf_uri,
            world)) for cf_body_name, cf_uri in zip(cf_body_names, cf_uris)]

    # Let there be time
    t = time()
    dt = 0

    print("Beginning maneuvers...")

    # MAIN LOOP WITH SAFETY CHECK
    while(next((False for qcf in qcfs if qcf.is_safe == False), True)):

        # Terminate upon Esc command
        if last_key_pressed == pynput.keyboard.Key.esc:
            break

        # Mind the clock
        dt = time() - t

        for idx, qcf in enumerate(qcfs):

            # Take off and hover in the center of safe airspace for 5 seconds
            if dt < 2:
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
                continue

            # Move out half of the safe airspace in the X direction and circle around Z axis
            if dt < 10:
                print(f'[t={int(dt)}] Maneuvering - Circle around Z...')
                # Set target
                phi = 2 * 360 * (dt-5) / 5  # Calculate angle based on time
                phi = phi + (360 / len(qcfs)) * (idx / (len(qcfs) + 1)) # Offset angle based on array
                _x, _y = utils.pol2cart(0.5, phi)
                target = Pose(world.origin.x + _x,
                              world.origin.y + _y,
                              world.expanse)
                # Engage
                qcf.safe_position_setpoint(target)
                sleep(0.1)
                continue

            # Back to center
            if dt < 12:
                print(f'[t={int(dt)}] Maneuvering - Center...')
                # Set target
                target = Pose(world.origin.x, world.origin.y, world.expanse)
                # Engage
                qcf.safe_position_setpoint(target)
                sleep(0.1)
                continue

            # Move out half of the safe airspace in the Z direction and circle around Y axis
            if dt < 20:
                print(f'[t={int(dt)}] Maneuvering - Circle around X...')
                # Set target
                phi = 2 * 360 * (dt-5) / 5  # Calculate angle based on time
                _x, _z = utils.pol2cart(0.5, phi)
                target = Pose(world.origin.x + _x,
                              world.origin.y,
                              world.expanse + _z)
                # Engage
                qcf.safe_position_setpoint(target)
                sleep(0.1)
                continue

            # Back to center
            if dt < 22:
                print(f'[t={int(dt)}] Maneuvering - Center...')
                # Set target
                target = Pose(world.origin.x, world.origin.y, world.expanse)
                # Engage
                qcf.safe_position_setpoint(target)
                sleep(0.1)
                continue

            # Move out half of the safe airspace in the Z direction and circle around X axis
            if dt < 30:
                print(f'[t={int(dt)}] Maneuvering - Circle around X...')
                # Set target
                phi = 2 * 360 * (dt-5) / 5  # Calculate angle based on time
                _y, _z = utils.pol2cart(0.5, phi)
                target = Pose(world.origin.x,
                              world.origin.y + _y,
                              world.expanse + _z)
                # Engage
                qcf.safe_position_setpoint(target)
                sleep(0.1)
                continue

            # Back to center
            if dt < 32:
                print(f'[t={int(dt)}] Maneuvering - Center...')
                # Set target
                target = Pose(world.origin.x, world.origin.y, world.expanse)
                # Engage
                qcf.safe_position_setpoint(target)
                sleep(0.1)
                continue

            # 3D random walk in safe airspace
            if dt < 40:
                print(f'[t={int(dt)}] Maneuvering - Random...')
                # Set target
                step_size = 0.2  # in m
                _pose = qcf.pose
                target = Pose(_pose.x + random.randint(-1, 1) * step_size,
                              _pose.y + random.randint(-1, 1) * step_size,
                              _pose.z + random.randint(-1, 1) * step_size)
                # Engage
                qcf.safe_position_setpoint(target)
                sleep(0.5)
                continue

            # Back to center
            if dt < 42:
                print(f'[t={int(dt)}] Maneuvering - Center...')
                # Set target
                target = Pose(world.origin.x, world.origin.y, world.expanse)
                # Engage
                qcf.safe_position_setpoint(target)
                sleep(0.1)
                continue

        else:
            break

    # Land calmly
    qcf.land_in_place()
