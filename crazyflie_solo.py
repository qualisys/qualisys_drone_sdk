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
cf_uri = 'radio://0/80/1M'

# QTM rigid body names
cf_body_name = 'cf'

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


with QualisysCrazyflie(cf_body_name,
                       cf_uri,
                       world) as qcf:

    world.set_origin_xy(qcf.pose)

    # Let there be time
    t = time()
    dt = 0

    # FLY
    while(qcf.is_safe()):

        dt = time() - t

        # Execute maneuvers

        # 1) Take off and hover 1m above initial position for 30 seconds
        if dt < 30:
            target = Pose(0, 0, 1)
            qcf.safe_position_setpoint(target)

        # 2) Move out 50cm in the X direction and complete 2 circles around its initial position
        if 30 < dt < 60:
            phi = 360 * (dt-30) / 30  # Calculate angle based on time
            _x, _y = qfly.utils.pol2cart(0.5, phi)
            target = Pose(_x, _y, 1, phi)
            qcf.safe_position_setpoint(target)

        # 3) For 1 minute, move randomly within a cubic volume that is 1m on each side, centered 1m above its initial position
        if 60 < dt < 120:
            qcf.random_walk()

    # Land calmly
    qcf.land()
