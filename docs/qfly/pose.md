Module qfly.pose
================

Classes
-------

`Pose(x, y, z, roll=None, pitch=None, yaw=None, rotmatrix=None)`
:   Full pose data with euler angles or rotation matrix.

    ### Static methods

    `from_qtm_6d(qtm_6d)`
    :   Construct Pose from QTM 6D component.

    ### Methods

    `clamp(self, world)`
    :   Keep within safe airspace defined by world parameter.

    `distance_to(self, other_pose)`
    :   TBD

    `is_valid(self)`
    :   Check if any of the coodinates are NaN.