
"""
qfly | Qualisys Drone SDK Example Script: Interactive Crazyflie with Deck

The drone flies along the YZ plane while centered at 0 along the X plane.
The Y and Z coordinates track another Crazyflie body equipped with an
Active Marker Deck.
ESC to land at any time.
"""

import pynput
from time import sleep

from qfly import ParallelContexts, Pose, QualisysCrazyflie, QualisysDeck, World


# SETTINGS
cf_body_name = 'E7E7E7E701'  # QTM rigid body name
cf_uri = 'radio://0/80/2M/E7E7E7E701'  # Crazyflie address
cf_marker_ids = [11, 12, 13, 14]
deck_body_name = 'E7E7E7E7E7'
deck_uri = 'radio://0/80/2M/E7E7E7E7E7'
deck_marker_ids = [1, 2, 3, 4]


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

deck = QualisysDeck(deck_body_name,
                    deck_uri,
                    deck_marker_ids)

with ParallelContexts(*[qcf, deck]):

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
        if deck.pose is not None:
            y = deck.pose.y
            z = deck.pose.z
        target = Pose(x, y, z)
        # Engage
        qcf.safe_position_setpoint(target)
        sleep(0.02)
        continue

    # Land calmly
    qcf.land_in_place()
