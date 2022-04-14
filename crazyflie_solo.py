import random
import pynput
from time import sleep, time

from qfly import Pose, QualisysCrazyflie, World
import qfly


# SETTINGS
cf_body_name = 'cf'  # QTM rigid body names
cf_uri = 'radio://0/80/1M/E7E7E7E7E7'  # Crazyflie address


def on_press(key):
    """React to keyboard."""
    global fly
    if key == pynput.keyboard.Key.esc:
        fly = False

    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()


# Set up world - the World object comes with sane defaults
world = qfly.World()


# Prepare for liftoff
with QualisysCrazyflie(cf_body_name,
                       cf_uri,
                       world) as qcf:

    # Let there be time
    t = time()
    dt = 0

    print("Beginning maneuvers...")


    # MAIN LOOP WITH SAFETY CHECK
    while(qcf.is_safe()):

        # Mind the clock
        dt = time() - t


        # 1Take off and hover in the center of safe airspace for 5 seconds
        if dt < 2:
            print(f'[t={int(dt)}] Maneuvering - Center...')
            # Set target
            target = Pose(world.origin.x, world.origin.y, world.expanse)
            # Engage
            qcf.safe_position_setpoint(target)
            sleep(0.1)
            continue

        # Move out half of the safe airspace in the X direction and circle around Z axis
        if dt < 10:
            print(f'[t={int(dt)}] Maneuvering - Circle around Z...')
            # Set target
            phi = 2 * 360 * (dt-5) / 5  # Calculate angle based on time
            _x, _y = qfly.utils.pol2cart(0.5, phi)
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
            _x, _z = qfly.utils.pol2cart(0.5, phi)
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
            _y, _z = qfly.utils.pol2cart(0.5, phi)
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
            max_step = 0.2
            _pose = qcf.pose
            target = qfly.Pose(_pose.x + random.randint(-1, 1) * max_step,
                               _pose.y + random.randint(-1, 1) * max_step,
                               _pose.z + random.randint(-1, 1) * max_step)
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
