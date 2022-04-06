from qfly import Pose


class World:
    """Holds safety-critical information about the physical world"""

    def __init__(self,
                 buffer=0.15,  # in m
                 expanse=1.0,  # in m
                 origin=Pose(0, 0, 0),  # x, y, z in m
                 speed=1.0,  # in m/s
                 tolerance=0.5,  # in m
                 ):

        self.buffer = buffer
        self.expanse = expanse
        self.origin = origin
        self.speed = speed
        self.tolerance = tolerance

    def set_origin_xy(self, pose):
        self.origin.x = pose.x
        self.origin.y = pose.y