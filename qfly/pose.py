from qfly import utils


class Pose:
    """
    Full pose data with euler angles or rotation matrix.
    """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.roll = None
        self.pitch = None
        self.yaw = None
        self.rotmatrix = None

    @classmethod
    def from_qtm_6d(cls, qtm_6d):
        """
        Construct Pose from QTM 6D component.
        """
        qtm_rot = qtm_6d[1].matrix
        rotmatrix = [[qtm_rot[0], qtm_rot[3], qtm_rot[6]],
                     [qtm_rot[1], qtm_rot[4], qtm_rot[7]],
                     [qtm_rot[2], qtm_rot[5], qtm_rot[8]]]
        return cls(qtm_6d[0][0] / 1000,
                   qtm_6d[0][1] / 1000,
                   qtm_6d[0][2] / 1000,
                   rotmatrix=rotmatrix)

    def clamp(self, world):
        """
        Keep within safe airspace defined by world parameter.
        """
        self.x = max(world.origin.x - world.expanse + world.padding,
                     min(self.x, world.origin.x + world.expanse - world.padding))
        self.y = max(world.origin.y - world.expanse + world.padding,
                     min(self.y, world.origin.y + world.expanse - world.padding))
        self.z = max(0,
                     min(self.z, world.origin.z + (2 * world.expanse) - world.padding))

    def distance_to(self, other_point):
        """
        TBD
        """
        return utils.sqrt(
            (self.x - other_point.x) ** 2 +
            (self.y - other_point.y) ** 2 +
            (self.z - other_point.z) ** 2)

    def is_valid(self):
        """
        Check if any of the coodinates are NaN.
        """
        return self.x == self.x and self.y == self.y and self.z == self.z

    def __str__(self):
        """
        TBD
        """
        # return "x: {:6.2f} y: {:6.2f} z: {:6.2f} Roll: {:6.2f} Pitch: {:6.2f} Yaw: {:6.2f}".format(
        # self.x, self.y, self.z, self.roll, self.pitch, self.yaw)
        return f'x: {self.x} y: {self.y} z: {self.z} yaw: {self.yaw}'
