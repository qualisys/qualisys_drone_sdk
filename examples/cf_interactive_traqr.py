
"""
qfly | Qualisys Drone SDK Example Script: Interactive Crazyflie with Traqr

The drone flies along the YZ plane while centered at 0 along the X plane.
The Y and Z coordinates track a Traqr or other appropriately configured
rigid body.
ESC to land at any time.
"""

import pynput
from time import sleep

from qfly import ParallelContexts, Pose, QualisysCrazyflie, QualisysTraqr, World


# SETTINGS
cf_body_name = 'E7E7E7E701'  # QTM rigid body name
cf_uri = 'radio://0/80/2M/E7E7E7E701'  # Crazyflie address
cf_marker_ids = [11, 12, 13, 14]
traqr_body_name = 'traqr'


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
qcf = QualisysCrazyflie(cf_body_name,
                        cf_uri,
                        world,
                        marker_ids=cf_marker_ids)

traqr = QualisysTraqr(traqr_body_name)

with ParallelContexts(*[qcf, traqr]):

    print("Beginning maneuvers...")

    # MAIN LOOP WITH SAFETY CHECK
    while(qcf.is_safe()):

        # Terminate upon Esc command
        if last_key_pressed == pynput.keyboard.Key.esc:
            break
        # Take off and hover in the center of safe airspace for 5 seconds
        # Set target
        x = world.origin.x
        y = world.origin.y
        z = world.expanse
        if traqr.pose is not None:
            y = traqr.pose.y
            z = traqr.pose.z
        target = Pose(x, y, z)
        # Engage
        qcf.safe_position_setpoint(target)
        sleep(0.02)
        continue

    # Land calmly
    qcf.land_in_place()
