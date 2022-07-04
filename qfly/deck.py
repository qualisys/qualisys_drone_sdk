from threading import Thread
import traceback

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

import qfly


class QualisysDeck(Thread):
    """
    Wrapper for Active Marker Deck-equipped Crazyflie drone
    used as a tracker without flying

    Attributes
    ----------
    cf_body_name : str
        Name of Crazyflie's rigid body in QTM
    cf_uri : str
        Crazyflie radio address
    pose : Pose
        Pose object keeping track of whereabouts
    """

    def __init__(self,
                 cf_body_name,
                 cf_uri,
                 marker_ids=[1, 2, 3, 4],
                 qtm_ip="127.0.0.1"):
        """
        Construct QualisysDeck object

        Parameters
        ----------
        cf_body_name : str
            Name of Crazyflie's rigid body in QTM
        cf_uri : str
            Crazyflie radio address
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
        self.marker_ids = marker_ids

        self.pose = None

        self.qtm = None
        self.qtm_ip = qtm_ip

        self.cf = Crazyflie(ro_cache=None, rw_cache=None)
        self.scf = SyncCrazyflie(self.cf_uri, cf=self.cf)

        print(f'[{self.cf_body_name}@{self.cf_uri}] Connecting...')

    def __enter__(self):
        """
        Enter QualisysDeck context
        """

        self.scf.open_link()

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

        self.qtm = qfly.QtmWrapper(
            self.cf_body_name,
            lambda pose: self._set_pose(pose),
            qtm_ip=self.qtm_ip)

        print(
            f'[{self.cf_body_name}@{self.cf_uri}] Connecting to QTM at {self.qtm.qtm_ip}...')

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

    def _set_pose(self, pose):
        """
        Set internal Pose object

        Parameters
        ----------
        pose : Pose
            Pose object containing coordinates
        """
        self.pose = pose
