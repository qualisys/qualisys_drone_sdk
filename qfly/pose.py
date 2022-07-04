from qfly import utils


class Pose:
    """
    Full pose data with euler angles or rotation matrix.
    """

    def __init__(self, x, y, z, roll=None, pitch=None, yaw=None, rotmatrix=None):
        self.x = x
        self.y = y
        self.z = z

        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
        self.rotmatrix = rotmatrix

    @classmethod
    def from_qtm_6d(cls, qtm_6d):
        """
        Constructs Pose from QTM 6D component.

        Parameters
        ----------
        qtm_6d
            6D pose data from QTM component
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
        Geofences pose within safe airspace
        defined by world parameter.

        Parameters
        ----------
        world : World
            World object defining airspace rules.
        """
        self.x = max(world.origin.x - world.expanse + world.padding,
                     min(self.x, world.origin.x + world.expanse - world.padding))
        self.y = max(world.origin.y - world.expanse + world.padding,
                     min(self.y, world.origin.y + world.expanse - world.padding))
        self.z = max(0,
                     min(self.z, world.origin.z + (2 * world.expanse) - world.padding))

    def distance_to(self, other_pose):
        """
        Returns distance between coordinates
        represented by two Pose objects.

        Parameters
        ----------
        other_pose : Pose
            Target Pose to measure distance between.
        """
        return utils.sqrt(
            (self.x - other_pose.x) ** 2 +
            (self.y - other_pose.y) ** 2 +
            (self.z - other_pose.z) ** 2)

    def is_valid(self):
        """
        Checks if any of the coodinates are NaN.
        """
        return self.x == self.x and self.y == self.y and self.z == self.z

    def __str__(self):
        # return "x: {:6.2f} y: {:6.2f} z: {:6.2f} Roll: {:6.2f} Pitch: {:6.2f} Yaw: {:6.2f}".format(
        # self.x, self.y, self.z, self.roll, self.pitch, self.yaw)
        return f'x: {self.x} y: {self.y} z: {self.z} yaw: {self.yaw}'
