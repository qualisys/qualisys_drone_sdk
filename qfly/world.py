from qfly import Pose


class World:
    """
    Hold safety-critical information about the physical world.
    """

    def __init__(self,
                 origin=Pose(0, 0, 0),  # x, y, z in m
                 expanse=1.0,  # in m
                 padding=0.15,  # in m
                 speed_limit=0.4,  # in m/s
                 tracking_tolerance=100  # in frames
                 ):
        """
        Construct World object

        Parameters
        ----------
        origin : Pose
            Pose object containing x, y, z coordinates of origin.
        expanse : float
            Edge dimension of cubic "safe" airspace extending from origin.
            (Unit: m)
        padding : float
            Safety tolerance at expanse boundary.
            (Unit: m)
        speed_limit : float
            Max allowed airspeed in horizontal (xy) 
            and vertical (z) dimensions.
            (Unit: m/s)
        tracking_tolerance : int
            Max allowed mocap frame loss.
            (Unit: frames)
        """

        self.origin = origin
        self.expanse = expanse
        self.padding = padding
        self.speed_limit = speed_limit
        self.tracking_tolerance = tracking_tolerance

    def set_origin_xy(self, pose):
        """
        Move World origin to new coordinates

        Parameters
        ----------
        pose : Pose
            Pose object containing x, y, z coordinates of new origin
        """
        self.origin = pose
