"""
qfly | Qualisys Drone SDK Example Script: Drone Pong

UNSTABLE / EXPERIMENTAL / UNDER DEVELOPMENT
"""

import math
import pynput
from time import sleep, time

from qfly import ParallelContexts, Pose, QualisysCrazyflie, QualisysDeck, World


# SETTINGS
cf_body_name = 'E7E7E7E706'
cf_uri = 'radio://0/80/2M/E7E7E7E706'
cf_marker_ids = [41, 62, 63, 64]

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
world = World(expanse=1.5, speed_limit=1, padding=0.3)

vx = 1
vy = 1
r_paddle = 0.5
bounce_angle_max = 1.5  # in radians


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

    # Let there be time
    t = time()
    dt = 0

    # MAIN LOOP WITH SAFETY CHECK
    while(qcf.is_safe()):

        # Mind the clock
        dt = time() - t

        # Terminate upon Esc command
        if last_key_pressed == pynput.keyboard.Key.esc:
            break
        
        if dt < 5:
            qcf.rise_in_place()
            continue

        # Bouncing algorithm for paddle hits
        if deck.pose is not None and qcf.pose is not None:
            if deck.pose.distance_to(qcf.pose) < r_paddle:
                relative_intersect_y = deck.pose.y + r_paddle - qcf.pose.y
                normalized_relative_intersect_y = relative_intersect_y / r_paddle
                bounce_angle = normalized_relative_intersect_y * bounce_angle_max
                # vx = abs(world.speed_limit * math.cos(bounce_angle))
                vx = 1.0
                vy = world.speed_limit * math.cos(bounce_angle)

        # Bouncing Algorithm when the Ball hit the edge of the canvas
        if qcf.pose.x > world.expanse - world.padding and vx > 0:
            vx = -vx
        if qcf.pose.x < -world.expanse + world.padding and vx < 0:
            vx = -vx
        if qcf.pose.y > world.expanse - world.padding and vy > 0:
            vy = -vy
        if qcf.pose.y < -world.expanse + world.padding and vy < 0:
            vy = -vy

        # Set target
        x = qcf.pose.x + vx
        y = qcf.pose.y + vy
        print(x)
        print(vx)
        print(y)
        print(vy)
        target = Pose(x, y, 1)
        # Engage
        qcf.safe_position_setpoint(target)

    # Land calmly
    qcf.land_in_place()
