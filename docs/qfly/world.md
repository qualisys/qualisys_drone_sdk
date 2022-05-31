Module qfly.world
=================

Classes
-------

`World(origin=<qfly.pose.Pose object>, expanse=1.0, padding=0.15, speed_limit=0.4, tracking_tolerance=100)`
:   Hold safety-critical information about the physical world
    
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
    
    TBD

    ### Methods

    `set_origin_xy(self, pose)`
    :   TBD