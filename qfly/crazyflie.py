from threading import Thread
import time
import traceback

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

import qfly


class QualisysCrazyflie(Thread):
    """
    Wrapper for Crazyflie drone to fly with Qualisys motion capture systems

    Attributes
    ----------
    cf_body_name : str
        Name of Crazyflie's rigid body in QTM
    cf_uri : str
        Crazyflie radio address
    pose : Pose
        Pose object keeping track of whereabouts
    world : World
        World object defining airspace rules
    """

    def __init__(self,
                 cf_body_name,
                 cf_uri,
                 world,
                 marker_ids=[1, 2, 3, 4],
                 qtm_ip="127.0.0.1"):
        """
        Construct QualisysCrazyflie object

        Parameters
        ----------
        cf_body_name : str
            Name of Crazyflie's rigid body in QTM
        cf_uri : str
            Crazyflie radio address
        world : World
            World object defining airspace rules
        qtm_ip : str
            IP address of QTM host.
        marker_ids : [int]
            ID numbers to be assigned to active markers
            in order of front, right, back, left
        """

        print(f'[{cf_body_name}@{cf_uri}] Initializing...')

        cflib.crtp.init_drivers()

        self.cf_body_name = cf_body_name
        self.cf_uri = cf_uri
        self.world = world
        self.marker_ids = marker_ids

        self.pose = None
        self.anchor = None

        self.qtm = None
        self.qtm_ip = qtm_ip

        self.cf = Crazyflie(ro_cache=None, rw_cache=None)
        self.scf = SyncCrazyflie(self.cf_uri, cf=self.cf)

        print(f'[{self.cf_body_name}@{self.cf_uri}] Connecting...')

    def __enter__(self):
        """
        Enter QualisysCrazyflie context
        """

        # self.scf = SyncCrazyflie(self.cf_uri)
        self.scf.open_link()
        # self.cf = self.scf.cf

        print(f'[{self.cf_body_name}@{self.cf_uri}] Connected...')

        # Set active marker IDs
        print(
            f'[{self.cf_body_name}@{self.cf_uri}] Setting active marker IDs: {self.marker_ids}')
        self.cf.param.set_value('activeMarker.front', self.marker_ids[0])
        self.cf.param.set_value('activeMarker.right', self.marker_ids[1])
        self.cf.param.set_value('activeMarker.back', self.marker_ids[2])
        self.cf.param.set_value('activeMarker.left', self.marker_ids[3])

        # Turn off LED to conserve battery
        self.set_led_ring(0)

        # Slow down
        self.set_speed_limit(self.world.speed_limit)

        self.qtm = qfly.QtmWrapper(
            self.cf_body_name,
            lambda pose: self._set_pose(pose),
            qtm_ip=self.qtm_ip)

        print(
            f'[{self.cf_body_name}@{self.cf_uri}] Connecting to QTM at {self.qtm.qtm_ip}...')

        self.setup()

        return self

    def __exit__(self, exc_type=None, exc_value=None, tb=None):
        """
        Exit QualisysCrazyflie context
        """
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

        Parameters
        ----------
        world : World (optional) 
            World object defining airspace rules.
            Defaults to object's own world if not supplied.
        """
        if world is None:
            world = self.world
        # Is the drone tracked properly?
        if self.qtm.tracking_loss > world.tracking_tolerance:
            # Respond
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
            # Respond
            print(f'''[{self.cf_body_name}@{self.cf_uri}] !!! SAFETY VIOLATION !!!
                DRONE OUTSIDE SAFE VOLUME AT ({str(self.pose)})!''')
            return False
        else:
            return True

    def ascend(self, z_ceiling=1, step=12.0):
        """
        Execute one step of a gentle rising sequence directly upward from current position.

        Parameters
        ----------
        z_ceiling : float (optional) 
            Height to ascend to. (unit: m)
        step : int (optional)
            Distance between target keyframes. Defaults to 3. (unit: cm)
        """
        init_pose = self.pose
        _z_cm = int(init_pose.z * 100)

        target = qfly.Pose(init_pose.x,
                           init_pose.y,
                           min(z_ceiling, float((_z_cm + step) / 100.0)))

        # print(
        #     f'[{self.cf_body_name}@{self.cf_uri}] Ascending from {_z_cm} cm to {z_ceiling}...')
        self.safe_position_setpoint(target)

    def descend(self, z_floor=0.0, step=12.0):
        """
        Execute one step of a gentle landing sequence directly downward from current position.

        Parameters
        ----------
        z_floor : float (optional) 
            Height to descend to. (unit: m)
        step : int (optional)
            Distance between target keyframes. Defaults to 3. (unit: cm)
        """
        init_pose = self.pose
        _z_cm = int(init_pose.z * 100)

        target = qfly.Pose(init_pose.x,
                           init_pose.y,
                           float((_z_cm - step) / 100.0))

        # Engage
        if target.z < z_floor:
            self.cf.commander.send_stop_setpoint()
        else:
            # print(
            #     f'[{self.cf_body_name}@{self.cf_uri}] Descending from {_z_cm} cm to {z_floor} cm...')
            self.safe_position_setpoint(target)

    def land_in_place(self):
        """
        Land sequence directly downward from current position.
        """
        if self.anchor is None or self.anchor.distance_to(self.pose) > self.world.padding:
            self.anchor = self.pose

        print(
            f'[{self.cf_body_name}@{self.cf_uri}] Landing to ground...')

        target = qfly.Pose(self.anchor.x, self.anchor.y, 0)

        if self.pose.distance_to(target) < 0.1:
            self.anchor = None
            self.cf.commander.send_stop_setpoint()
        else:
            self.safe_position_setpoint(target)

    def land_to_moving_target(self, target, z_offset=0.5, decrement=3, timestep=0.15):
        """
        FIXME: DO NOT USE. NOT SUITABLE FOR MULTIPLE DRONES.
        Execute a gentle landing sequence aiming at a live target.

        Parameters
        ----------
        target : object
            An object that has a pose attribute
        z_offset : float (optional)
            Vertical offset between target and landing start pose. (unit: m, default: 0.5)
        decrement : int (optional)
            Distance between target keyframes. (unit: cm, default: 3)
        timestep : float (optional
            Time between target keyframes. (unit: s, default: 0.15)
        """
        try:
            init_pose = qfly.Pose(target.pose.x,
                                  target.pose.y,
                                  target.pose.z + z_offset)
        except AttributeError:
            print(f'''[{self.cf_body_name}@{self.cf_uri}] !!! ERROR !!!
                Landing target has no pose attribute! Landing in place instead!''')
            self.land_in_place()
            return

        z_cm = int(init_pose.z * 100)

        print(
            f'[{self.cf_body_name}@{self.cf_uri}] Landing to live target from {z_cm} cm...')

        # Linear interpolation between starting pose and target
        while z_cm > target.pose.z * 100:
            target = qfly.Pose(target.pose.x, target.pose.y,
                               float(z_cm / 100.0))
            self.safe_position_setpoint(target)
            time.sleep(timestep)
            z_cm = z_cm - decrement
        self.cf.commander.send_stop_setpoint()

    def rise_in_place(self, z=1):
        """
        Ascension sequence directly upwards from current position.

        Parameters
        ----------
        z_ceiling : float (optional) 
            Height to ascend to. (unit: m)
        """
        if self.anchor is None or self.anchor.distance_to(self.pose) > self.world.padding:
            self.anchor = self.pose

        print(
            f'[{self.cf_body_name}@{self.cf_uri}] Ascending...')

        target = qfly.Pose(self.anchor.x, self.anchor.y, z)

        self.safe_position_setpoint(target)

    def safe_position_setpoint(self, target, world=None):
        """
        Set a clean absolute position setpoint
        within safe airspace defined by world.

        Parameters
        ----------
        target : Pose
            Pose object bearting target coordinate and yaw.
            Yaw defaults to 0 if not supplied.
        world : World (optional)
            World object defining airspace rules.
            Defaults to object's own world if not supplied.
        """
        # Sane defaults
        if world is None:
            world = self.world
        if target.yaw == None:
            target.yaw = 0
        # Keep inside safe airspace
        target.clamp(world)
        # Engage
        self.cf.commander.send_position_setpoint(
            target.x, target.y, target.z, target.yaw)

    def setup(self):
        """
        Execute drone engineering boilerplate.
        Assumes most drone parameters at factory defaults.
        If in doubt, inspect drone parameters
        using Bitcraze client and documentation.
        """
        print(f'[{self.cf_body_name}@{self.cf_uri}] Setting up drone...')

        # Choose estimator
        self.cf.param.set_value('stabilizer.estimator', '2')

        # Black magic
        self.cf.param.set_value('locSrv.extQuatStdDev', 0.06)

        # Reset estimator
        self.cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        self.cf.param.set_value('kalman.resetEstimation', '0')

        # Stabilize
        print(
            f'[{self.cf_body_name}@{self.cf_uri}] Stabilizing...')

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

    def set_led_ring(self, val):
        """
        Set LED ring effect.

        Parameters
        ----------
        val : int
            LED ring effect ID. See Bitcraze documentation:
            https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/params/#ring
        """
        self.cf.param.set_value('ring.effect', val)

    def set_speed_limit(self, speed_limit):
        """
        Set speed limit.

        Parameters
        ----------
        speed_limit : float
            Limit for horizontal (xy) and vertical (z) speed. (unit: m/s)
        """
        print(f'[{self.cf_body_name}@{self.cf_uri}] Speed limit: {speed_limit} m/s')
        self.cf.param.set_value('posCtlPid.xyVelMax', speed_limit)
        self.cf.param.set_value('posCtlPid.zVelMax', speed_limit)

    def _set_pose(self, pose):
        """
        Set internal Pose object and stream to drone

        Parameters
        ----------
        pose : Pose
            Pose object containing coordinates
        """
        self.pose = pose
        # Send to Crazyflie
        if self.cf is not None:
            self.cf.extpos.send_extpos(pose.x, pose.y, pose.z)
