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
cf_marker_ids = [1, 2, 3, 4] # Active marker IDs
circle_radius = 0.5 # Radius of the circular flight path
circle_speed_factor = 0.12 # How fast the Crazyflie should move along circle


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

        # Calculate Crazyflie's angular position in circle, based on time
        phi = circle_speed_factor * dt * 360


        # Take off and hover in the center of safe airspace for 5 seconds
        if dt < 5:
            print(f'[t={int(dt)}] Maneuvering - Center...')
            # Set target
            target = Pose(world.origin.x, world.origin.y, world.expanse)
            # Engage
            qcf.safe_position_setpoint(target)

        # Move out and circle around Z axis
        elif dt < 20:
            print(f'[t={int(dt)}] Maneuvering - Circle around Z...')
            # Set target
            _x, _y = utils.pol2cart(circle_radius, phi)
            target = Pose(world.origin.x + _x,
                          world.origin.y + _y,
                          world.expanse)
            # Engage
            qcf.safe_position_setpoint(target)

        # Back to center
        elif dt < 25:
            print(f'[t={int(dt)}] Maneuvering - Center...')
            # Set target
            target = Pose(world.origin.x, world.origin.y, world.expanse)
            # Engage
            qcf.safe_position_setpoint(target)

        # Move out and circle around Y axis
        elif dt < 40:
            print(f'[t={int(dt)}] Maneuvering - Circle around X...')
            # Set target
            _x, _z = utils.pol2cart(circle_radius, phi)
            target = Pose(world.origin.x + _x,
                          world.origin.y,
                          world.expanse + _z)
            # Engage
            qcf.safe_position_setpoint(target)

        # Back to center
        elif dt < 45:
            print(f'[t={int(dt)}] Maneuvering - Center...')
            # Set target
            target = Pose(world.origin.x, world.origin.y, world.expanse)
            # Engage
            qcf.safe_position_setpoint(target)

        # Move and circle around X axis
        elif dt < 60:
            print(f'[t={int(dt)}] Maneuvering - Circle around X...')
            # Set target
            _y, _z = utils.pol2cart(circle_radius, phi)
            target = Pose(world.origin.x,
                          world.origin.y + _y,
                          world.expanse + _z)
            # Engage
            qcf.safe_position_setpoint(target)

        # Back to center
        elif dt < 65:
            print(f'[t={int(dt)}] Maneuvering - Center...')
            # Set target
            target = Pose(world.origin.x, world.origin.y, world.expanse)
            # Engage
            qcf.safe_position_setpoint(target)

        else:
            break

    # Land
    while (qcf.pose.z > 0.1):
        qcf.land_in_place()