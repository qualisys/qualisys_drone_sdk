class Pose:
    """Holds pose data with euler angles and/or rotation matrix"""
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
        """Build pose from rigid body data in QTM 6d component"""
        qtm_rot = qtm_6d[1].matrix
        cf_rot = [[qtm_rot[0], qtm_rot[3], qtm_rot[6]],
                  [qtm_rot[1], qtm_rot[4], qtm_rot[7]],
                  [qtm_rot[2], qtm_rot[5], qtm_rot[8]]]
        return cls(qtm_6d[0][0] / 1000,
                   qtm_6d[0][1] / 1000,
                   qtm_6d[0][2] / 1000,
                   rotmatrix = cf_rot)

    @classmethod
    def from_qtm_6deuler(cls, qtm_6deuler):
        """Build pose from rigid body data in QTM 6deuler component"""
        return cls(qtm_6deuler[0][0] / 1000,
                   qtm_6deuler[0][1] / 1000,
                   qtm_6deuler[0][2] / 1000,
                   roll  = qtm_6deuler[1][2],
                   pitch = qtm_6deuler[1][1],
                   yaw   = qtm_6deuler[1][0])

    def distance_to(self, other_point):
        return sqrt(
            (self.x - other_point.x) ** 2 +
            (self.y - other_point.y) ** 2 +
            (self.z - other_point.z) ** 2)

    def is_valid(self):
        """Check if any of the coodinates are NaN."""
        return self.x == self.x and self.y == self.y and self.z == self.z

    def __str__(self):
        return "x: {:6.2f} y: {:6.2f} z: {:6.2f} Roll: {:6.2f} Pitch: {:6.2f} Yaw: {:6.2f}".format(
            self.x, self.y, self.z, self.roll, self.pitch, self.yaw)