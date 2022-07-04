from threading import Thread
import traceback

import qfly


class QualisysTraqr(Thread):
    """
    Wrapper for convenient operation of the Qualisys Traqr

    Attributes
    ----------
    trqr_body_name : str
        Name of Crazyflie's rigid body in QTM
    pose : Pose
        Pose object keeping track of whereabouts
    """

    def __init__(self,
                 traqr_body_name,
                 qtm_ip="127.0.0.1"):
        """
        Construct QualisysTraqr object

        Parameters
        ----------
        traqr_body_name : str
            Name of Traqr's rigid body in QTM
        qtm_ip : str
            IP address of QTM host.
        """

        print(f'[TRAQR {traqr_body_name}] Initializing...')

        self.traqr_body_name = traqr_body_name

        self.pose = None
        self.qtm = None
        self.qtm_ip = qtm_ip

        print(f'[TRAQR {self.traqr_body_name}]  Connecting...')

    def __enter__(self):
        """
        Enter QualisysTraqr context
        """
        print(f'[TRAQR {self.traqr_body_name}]  Setting up...')

        self.qtm = qfly.QtmWrapper(
            self.traqr_body_name,
            lambda pose: self._set_pose(pose),
            qtm_ip=self.qtm_ip)

        print(
            f'[TRAQR {self.traqr_body_name}] Connecting to QTM at {self.qtm.qtm_ip}...')

        return self

    def __exit__(self, exc_type=None, exc_value=None, tb=None):
        """
        Exit QualisysTraqr context
        """
        print(
            f'[TRAQR {self.traqr_body_name}] Exiting...')
        if exc_type is not None:
            print(
                f'[TRAQR {self.traqr_body_name}] Encountered exception on exit...')
            traceback.print_exception(exc_type, exc_value, tb)
        self.qtm.close()

    def _set_pose(self, pose):
        """
        Set internal Pose object

        Parameters
        ----------
        pose : Pose
            Pose object containing coordinates
        """
        self.pose = pose
