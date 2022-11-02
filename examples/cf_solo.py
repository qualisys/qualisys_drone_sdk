"""
qfly | Qualisys Drone SDK Example Script: Solo Crazyflie

Takes off, flies circles around Z, Y, X axes.
ESC to land at any time.
"""


import pynput
from time import sleep, time

from qfly import Pose, QualisysCrazyflie, World, utils


# SETTINGS
cf_body_name = 'Crazyflie'  # QTM rigid body name
cf_uri = 'radio://0/80/2M/E7E7E7E7E7'  # Crazyflie address
cf_marker_ids = [1, 2, 3, 4]


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

    # MAIN LOOP WITH SAFETY CHECK
    while(qcf.is_safe()):

        # Terminate upon Esc command
        if last_key_pressed == pynput.keyboard.Key.esc:
            break

        # Mind the clock
        dt = time() - t

        # Take off and hover in the center of safe airspace for 5 seconds
        if dt < 3:
            print(f'[t={int(dt)}] Maneuvering - Center...')
            # Set target
            target = Pose(world.origin.x, world.origin.y, world.expanse)
            # Engage
            qcf.safe_position_setpoint(target)
            sleep(0.02)

        # Move out half of the safe airspace in the X direction and circle around Z axis
        elif dt < 10:
            print(f'[t={int(dt)}] Maneuvering - Circle around Z...')
            # Set target
            phi = 2 * 360 * (dt-5) / 5  # Calculate angle based on time
            _x, _y = utils.pol2cart(0.5, phi)
            target = Pose(world.origin.x + _x,
                          world.origin.y + _y,
                          world.expanse)
            # Engage
            qcf.safe_position_setpoint(target)
            sleep(0.02)

        # Back to center
        elif dt < 13:
            print(f'[t={int(dt)}] Maneuvering - Center...')
            # Set target
            target = Pose(world.origin.x, world.origin.y, world.expanse)
            # Engage
            qcf.safe_position_setpoint(target)
            sleep(0.02)

        # Move out half of the safe airspace in the Z direction and circle around Y axis
        elif dt < 20:
            print(f'[t={int(dt)}] Maneuvering - Circle around X...')
            # Set target
            phi = 2 * 360 * (dt-5) / 5  # Calculate angle based on time
            _x, _z = utils.pol2cart(0.5, phi)
            target = Pose(world.origin.x + _x,
                          world.origin.y,
                          world.expanse + _z)
            # Engage
            qcf.safe_position_setpoint(target)
            sleep(0.02)

        # Back to center
        elif dt < 23:
            print(f'[t={int(dt)}] Maneuvering - Center...')
            # Set target
            target = Pose(world.origin.x, world.origin.y, world.expanse)
            # Engage
            qcf.safe_position_setpoint(target)
            sleep(0.02)

        # Move out half of the safe airspace in the Z direction and circle around X axis
        elif dt < 30:
            print(f'[t={int(dt)}] Maneuvering - Circle around X...')
            # Set target
            phi = 2 * 360 * (dt-5) / 5  # Calculate angle based on time
            _y, _z = utils.pol2cart(0.5, phi)
            target = Pose(world.origin.x,
                          world.origin.y + _y,
                          world.expanse + _z)
            # Engage
            qcf.safe_position_setpoint(target)
            sleep(0.02)

        # Back to center
        elif dt < 33:
            print(f'[t={int(dt)}] Maneuvering - Center...')
            # Set target
            target = Pose(world.origin.x, world.origin.y, world.expanse)
            # Engage
            qcf.safe_position_setpoint(target)
            sleep(0.02)

        else:
            break

    # Land
    while (qcf.pose.z > 0.1):
        qcf.land_in_place()
        sleep(0.02)