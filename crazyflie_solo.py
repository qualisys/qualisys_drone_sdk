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

from pynput import keyboard

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

import quadkit_crazyflie as qk

#
# SETTINGS
#

# Network addresses
cf_uri = 'radio://0/80/2M'

# QTM rigid body names
cf_body_name = 'CF'

# Physical space config
x_min = -2.0  # in m
x_max = 2.0  # in m
y_min = -2.0  # in m
y_max = 2.0  # in m
z_min = 0.0  # in m
z_max = 2.0  # in m
safeZone_margin = 0.5  # in m
cf_max_vel = 1  # in m/s
cf_trackingLoss_treshold = 200


#
# GLOBAL VARS
#

fly = True
cf_trackingLoss = 0
cf_pose = qk.Pose(0, 0, 0)


#
# ACTION
#

def on_press(key):
    """React to keyboard."""
    global fly, controller_offset_x, controller_offset_y, controller_offset_z, controller_select, land_to_target
    if key == keyboard.Key.esc:
        fly = False


# Init Crazyflie drivers
cflib.crtp.init_drivers(enable_debug_driver=False)

# Connect to QTM
qtm_wrapper = qk.QtmWrapper()


with SyncCrazyflie(cf_uri, cf=Crazyflie(rw_cache='./cache')) as scf:
    print(f'Connected to Crazyflie at "{cf_uri}"...')
    
    cf = scf.cf

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Slow down
    cf.param.set_value('posCtlPid.xyVelMax', cf_max_vel)
    cf.param.set_value('posCtlPid.zVelMax', cf_max_vel)

    # Set active marker IDs

    # Set up callbacks to handle data from QTM
    qtm_wrapper.on_cf_pose = lambda pose: qk.send_extpose_rot_matrix(
        cf, pose[0], pose[1], pose[2], pose[3])

    qk.setup_estimator(scf)

    # Let there be time
    t = time()
    dt = 0

    # FLY
    while(fly == True):

        dt = time() - t

        # Land if drone strays out of bounding box
        if not (x_min - safeZone_margin < cf_pose.x < x_max + safeZone_margin
           and y_min - safeZone_margin < cf_pose.y < y_max + safeZone_margin
           and z_min - safeZone_margin < cf_pose.z < z_max + safeZone_margin):
            print("DRONE HAS LEFT SAFE ZONE!")
            break
        # Land if drone disappears
        if cf_trackingLoss > cf_trackingLoss_treshold:
            print("TRACKING LOST FOR " +
                  str(cf_trackingLoss_treshold) + " FRAMES!")
            break

        # Execute maneuvers

        # 1= Take off and hover 1m above initial position for 30 seconds
        if dt < 30:
            # Do flying things
            continue


        # Move out 50cm in the X direction and complete 2 circles around its initial position
        if 30 < dt < 30:

        # For 1 minute, move randomly within a cubic volume that is 1m on each side, centered 1m above its initial position

        # Compute target
        target_pose = qk.Pose(
            controller_pose.x + controller_offset_x,
            controller_pose.y + .controller_offset_y,
            controller_pose.z + controller_offset_z,
            yaw=0
        )

        # Keep target inside bounding box
        target_pose.x = max(x_min, min(target_pose.x, x_max))
        target_pose.y = max(y_min, min(target_pose.y, y_max))
        target_pose.z = max(z_min, min(target_pose.z, z_max))

        # Go to target
        cf.commander.send_position_setpoint(
            target_pose.x, target_pose.y, target_pose.z, target_pose.yaw)

    # Land calmly
    print("Landing...")

    # Slow down
    cf.param.set_value('posCtlPid.xyVelMax', 0.3)
    cf.param.set_value('posCtlPid.zVelMax', 0.03)
    time.sleep(0.1)

    for z in range(5, 0, -1):
        cf.commander.send_hover_setpoint(0, 0, 0, float(z) / 10.0)
        time.sleep(0.15)

qtm_wrapper.close()
