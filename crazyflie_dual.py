# -*- coding: utf-8 -*-
#
#  Copyright (C) 2022 Qualisys AB
#  Portions (C) 2021 Weatherlight AB
#
#  Crazyflie x Qualisys Flight Demo
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.


import time
import pynput

from qfly import Pose, QualisysCrazyflie, World
import qfly

#
# SETTINGS
#

# Network addresses
cf_uris = [
    'radio://0/10/2M/E7E7E7E701',  # cf_id 0, startup position [-0.5, -0.5]
    'radio://0/10/2M/E7E7E7E702',  # cf_id 1, startup position [ 0, 0]
]

# QTM rigid body names
cf_body_names = ['cf1', 'cf2']

#
# ACTION
#

world = qfly.World()


def on_press(key):
    """React to keyboard."""
    global fly
    if key == pynput.keyboard.Key.esc:
        fly = False

    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()


with (QualisysCrazyflie(cf_body_names[0], cf_uris[0], world) as qcf_0,
      QualisysCrazyflie(cf_body_names[1], cf_uris[1], world) as qcf_1):

    qcf_0.set_world_origin()

    # Let there be time
    t = time()
    dt = 0

    # FLY
    while(fly == True):

        dt = time() - t

        # Execute maneuvers

        # 1= Take off and hover 1m above initial position for 30 seconds
        if dt < 30:
            # Do flying things
            target_0 = Pose(0, 0, 1)
            # FIGURE OUT HOW TO BREAK THE LOOP FROM HERE
            qcf_0.safe_position_setpoint(target_0)

            target_1 = Pose(1, 0, 1)
            qcf_1.safe_position_setpoint(target_1)

        # Move out 50cm in the X direction and complete 2 circles around its initial position
        # if 30 < dt < 30:

        # For 1 minute, move randomly within a cubic volume that is 1m on each side,
        # centered 1m above its initial position

    # Land calmly
    qcf_0.land()
    qcf_1.land()