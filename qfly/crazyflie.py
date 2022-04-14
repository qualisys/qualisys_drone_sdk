import math
from threading import Thread
import time
import traceback

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

import qfly
from qfly.utils import sqrt


class QualisysCrazyflie(Thread):
    """Wrapper for Crazyflie drone to fly with Qualisys motion capture systems

    Attributes
    ----------
    cf_body_name : string
        Pose object containing x, y, z coordinates of origin
    cf_uri : string
        radius of "safe" airspace extending from origin (unit: m)
    world : World
        World object setting airspace rules

    Methods
    -------
    TBD
    """

    def __init__(self,
                 cf_body_name,
                 cf_uri,
                 world,
                 max_vel=1.0):
        #  marker_ids=[101, 102, 103, 104]):
        print(f'[{cf_body_name}@{cf_uri}] Initializing...')

        # Init Crazyflie drivers
        cflib.crtp.init_drivers()

        self.cf = None
        self.cf_body_name = cf_body_name
        self.cf_uri = cf_uri
        # self.marker_ids = marker_ids
        self.max_vel = max_vel
        self.qtm = qfly.QtmWrapper(cf_body_name, lambda pose: self._set_pose(pose))
        self.pose = qfly.Pose(0, 0, 0)
        self.scf = SyncCrazyflie(cf_uri)
        self.world = world

        print(f'[{self.cf_body_name}@{self.cf_uri}] Connected.')
        print(
            f'[{self.cf_body_name}@{self.cf_uri}] Connecting to QTM: {self.qtm.qtm_ip}')

    def __enter__(self):
        self.scf.open_link()
        self.cf = self.scf.cf

        # Slow down
        self.set_speed_limit(self.world.speed_limit)

        # # Set active marker IDs
        # print(
        #     f'[{self.cf_body_name}@{self.cf_uri}] Active marker IDs: {self.marker_ids}')
        # self.cf.param.set_value('activeMarker.back', self.marker_ids[0])
        # self.cf.param.set_value('activeMarker.front', self.marker_ids[1])
        # self.cf.param.set_value('activeMarker.left', self.marker_ids[2])
        # self.cf.param.set_value('activeMarker.right', self.marker_ids[3])

        self.setup()

        return self

    def __exit__(self, exc_type, exc_value, tb):
        print(
            f'[{self.cf_body_name}@{self.cf_uri}] Exiting...')
        if exc_type is not None:
            print(
                f'[{self.cf_body_name}@{self.cf_uri}] Encountered exception on exit...')
            traceback.print_exception(exc_type, exc_value, tb)
        self.qtm.close()
        self.scf.close_link()

    def is_safe(self, world=None):
        """
        Perform safety checks, return False if unsafe

        Parameters:
            world (World): (Optional) World object specifying airspace rules.
                Defaults to QualisysCrazyflie's own world if not supplied.
        """
        if world is None:
            world = self.world
        # Is the drone tracked properly?
        if self.qtm.tracking_loss > world.tracking_tolerance:
            print(f'''[{self.cf_body_name}@{self.cf_uri}] !!! SAFETY VIOLATION !!!
                TRACKING LOST FOR {str(self.world.tracking_tolerance)} FRAMES!''')
            return False
        # Is the drone inside the safe volume?
        if not (
            # x direction
            world.origin.x - world.expanse < self.pose.x < world.origin.x + world.expanse
            # y direction
            and world.origin.y - world.expanse < self.pose.y < world.origin.y + world.expanse
            # z direction
                and 0 < self.pose.z < world.origin.z + (2 * world.expanse)):
            print(f'''[{self.cf_body_name}@{self.cf_uri}] !!! SAFETY VIOLATION !!!
                DRONE OUTSIDE SAFE VOLUME AT ({str(self.pose)})!''')
            return False
        else:
            return True

    def land_in_place(self):
        """
        Execute a gentle landing sequence directly down from current position
        """
        _pose = self.pose
        _z_cm = int(_pose.z * 100)

        print(f'[{self.cf_body_name}@{self.cf_uri}] Landing from {_z_cm} cm...')

        for z_cm in range(_z_cm, 0, -3):
            target = qfly.Pose(_pose.x, _pose.y, float(z_cm / 100.0))
            self.safe_position_setpoint(target)
            time.sleep(0.15)
        self.cf.commander.send_stop_setpoint()

    def safe_position_setpoint(self, target, world=None):
        """
        Set absolute position setpoint within safe airspace defined by world.

        Parameters:
            target (Pose): Pose object bearting target coordinate and yaw.
                Yaw defaults to 0 if not supplied.
            world (World): (Optional) World object specifying airspace rules.
                Defaults to QualisysCrazyflie's own world if not supplied.
        """
        # Sane defaults
        if world is None:
            world = self.world
        if target.yaw == None:
            target.yaw = 0
        # Keep inside safe airspace
        target.clamp(world)
        # Engage
        # self.cf.high_level_commander.go_to(
        #     target.x, target.y, target.z, target.yaw)
        self.cf.commander.send_position_setpoint(
            target.x, target.y, target.z, target.yaw)

    def setup(self):
        print(f'[{self.cf_body_name}@{self.cf_uri}] Setting up drone...')

        # Choose estimator
        self.cf.param.set_value('stabilizer.estimator', '2')
        self.cf.param.set_value('locSrv.extQuatStdDev', 0.06)

        # Choose commander
        # self.cf.param.set_value('commander.enHighLevel', '1')

        # Choose controller
        # self.cf.param.set_value('stabilizer.controller', '2')

        # Reset estimator
        self.cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        self.cf.param.set_value('kalman.resetEstimation', '0')

        # Wait for estimator to stabilize
        print(
            f'[{self.cf_body_name}@{self.cf_uri}] Waiting for estimator to stabilize...')

        log_config = LogConfig(name='Kalman Variance', period_in_ms=500)
        log_config.add_variable('kalman.varPX', 'float')
        log_config.add_variable('kalman.varPY', 'float')
        log_config.add_variable('kalman.varPZ', 'float')

        var_y_history = [1000] * 10
        var_x_history = [1000] * 10
        var_z_history = [1000] * 10

        threshold = 0.001

        with SyncLogger(self.scf, log_config) as logger:
            for log_entry in logger:
                data = log_entry[1]

                var_x_history.append(data['kalman.varPX'])
                var_x_history.pop(0)
                var_y_history.append(data['kalman.varPY'])
                var_y_history.pop(0)
                var_z_history.append(data['kalman.varPZ'])
                var_z_history.pop(0)

                min_x = min(var_x_history)
                max_x = max(var_x_history)
                min_y = min(var_y_history)
                max_y = max(var_y_history)
                min_z = min(var_z_history)
                max_z = max(var_z_history)

                print(f'[{self.cf_body_name}@{self.cf_uri}] ' +
                      "Kalman variance | X: {:8.4f}  Y: {:8.4f}  Z: {:8.4f}".format(
                          max_x - min_x, max_y - min_y, max_z - min_z))

                if (max_x - min_x) < threshold and (
                        max_y - min_y) < threshold and (
                        max_z - min_z) < threshold:
                    break

    def set_speed_limit(self, speed_limit):
        print(f'[{self.cf_body_name}@{self.cf_uri}] Speed limit: {speed_limit} m/s')
        self.cf.param.set_value('posCtlPid.xyVelMax', speed_limit)
        self.cf.param.set_value('posCtlPid.zVelMax', speed_limit)

    def _set_pose(self, pose):
        """
        Set internal Pose object and stream to drone
        """
        self.pose = pose
        # Send to Crazyflie
        if self.cf is not None:
            self.cf.extpos.send_extpos(pose.x, pose.y, pose.z)
