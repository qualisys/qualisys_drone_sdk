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

from qfly import Pose, World
from qfly.crazyflie import QualisysCrazyflie

#
# SETTINGS
#

# Network addresses
cf_uri = 'radio://0/80/1M'

# QTM rigid body names
cf_body_name = 'cf'

# Init physical space
world = World()


#
# GLOBAL VARS
#

fly = True

#
# ACTION
#

def on_press(key):
    """React to keyboard."""
    global fly
    if key == pynput.keyboard.Key.esc:
        fly = False
    
    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()


with QualisysCrazyflie(cf_body_name,
                       cf_uri,
                       world,
                       verbose=True) as qcf:

    # Let there be time
    t = time()
    dt = 0

    # FLY
    while(fly == True):

        dt = time() - t

        # Land if drone strays out of bounding box
        # if not (x_min - safeZone_margin < cf_pose.x < x_max + safeZone_margin
        #    and y_min - safeZone_margin < cf_pose.y < y_max + safeZone_margin
        #    and z_min - safeZone_margin < cf_pose.z < z_max + safeZone_margin):
        #     print("DRONE HAS LEFT SAFE ZONE!")
        #     break
        # # Land if drone disappears
        # if cf_trackingLoss > cf_trackingLoss_treshold:
        #     print("TRACKING LOST FOR " +
        #           str(cf_trackingLoss_treshold) + " FRAMES!")
        #     break

        # Execute maneuvers

        # 1= Take off and hover 1m above initial position for 30 seconds
        if dt < 30:
            # Do flying things
            target = Pose(0, 0, 1)
            qcf.safe_position_setpoint(target)

        # Move out 50cm in the X direction and complete 2 circles around its initial position
        # if 30 < dt < 30:

            # For 1 minute, move randomly within a cubic volume that is 1m on each side, centered 1m above its initial position

            # Compute target
        # target_pose = qf.Pose(
        #     controller_pose.x + controller_offset_x,
        #     controller_pose.y + .controller_offset_y,
        #     controller_pose.z + controller_offset_z,
        #     yaw=0
        # )

        # # Keep target inside bounding box
        # target_pose.x = max(x_min, min(target_pose.x, x_max))
        # target_pose.y = max(y_min, min(target_pose.y, y_max))
        # target_pose.z = max(z_min, min(target_pose.z, z_max))

        # # Go to target
        # cf.commander.send_position_setpoint(
        #     target_pose.x, target_pose.y, target_pose.z, target_pose.yaw)

    # Land calmly
    print("Landing...")

    # Slow down
    qcf.cf.param.set_value('posCtlPid.xyVelMax', 0.3)
    qcf.cf.param.set_value('posCtlPid.zVelMax', 0.03)
    time.sleep(0.1)

    for z in range(5, 0, -1):
        qcf.cf.commander.send_hover_setpoint(0, 0, 0, float(z) / 10.0)
        time.sleep(0.15)

qcf.qtm.close()
