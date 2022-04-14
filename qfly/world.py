from qfly import Pose


class World:
    """Hold safety-critical information about the physical world

    Attributes
    ----------
    origin : Pose
        Pose object containing x, y, z coordinates of origin
    expanse : float
        radius of "safe" airspace extending from origin (unit: m)
    padding : float
        safety tolerance at expanse boundary (unit: m)
    speed_limit : float
        max allowed airspeed (unit: m/s)
    tracking_tolerance : int
        max allowed mocap frame loss (unit: frames)

    Methods
    -------
    set_origin(pose):
        changes x, y, z coordinates of origin
    """

    def __init__(self,
                 origin=Pose(0, 0, 0),  # x, y, z in m
                 expanse=1.0,  # in m
                 padding=0.15,  # in m
                 speed_limit=0.4,  # in m/s
                 tracking_tolerance=150  # in frames
                 ):

        self.origin = origin
        self.expanse = expanse
        self.padding = padding
        self.speed_limit = speed_limit
        self.tracking_tolerance = tracking_tolerance

    def set_origin_xy(self, pose):
        self.origin = pose
