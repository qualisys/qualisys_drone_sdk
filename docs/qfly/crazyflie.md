Module qfly.crazyflie
=====================

Classes
-------

`QualisysCrazyflie(cf_body_name, cf_uri, world, marker_ids=[1, 2, 3, 4], qtm_ip='127.0.0.1')`
:   Wrapper for Crazyflie drone to fly with Qualisys motion capture systems
    
    Attributes
    ----------
    cf_body_name : str
        Name of Crazyflie's rigid body in QTM
    cf_uri : str
        Crazyflie radio address
    world : World
        World object defining airspace rules
    
    Construct QualisysCrazyflie object
    
    Parameters
    ----------
    cf_body_name : str
        Name of Crazyflie's rigid body in QTM
    cf_uri : str
        Crazyflie radio address
    world : World
        World object defining airspace rules
    qtm_ip : str
        IP address of QTM host.
    marker_ids : [int]
        ID numbers to be assigned to active markers
        in order of front, right, back, left

    ### Ancestors (in MRO)

    * threading.Thread

    ### Methods

    `ascend(self, z_ceiling=1, step=12.0)`
    :   Execute one step of a gentle ascension sequence directly upward from current position.
        
        Parameters
        ----------
        z_ceiling : float (optional) 
            Height to ascend to. (unit: m)
        step : int (optional)
            Distance between target keyframes. Defaults to 3. (unit: cm)

    `descend(self, z_floor=0.0, step=12.0)`
    :   Execute one step of a gentle descension sequence directly downward from current position.
        
        Parameters
        ----------
        z_floor : float (optional) 
            Height to descend to. (unit: m)
        step : int (optional)
            Distance between target keyframes. Defaults to 3. (unit: cm)

    `is_safe(self, world=None)`
    :   Perform safety checks, return False if unsafe
        
        Parameters
        ----------
        world : World (optional) 
            World object defining airspace rules.
            Defaults to object's own world if not supplied.

    `land_in_place(self, ground_z=0, decrement=3, timestep=0.15)`
    :   WARNING: DO NOT USE. NOT SUITABLE FOR MULTIPLE DRONES.
        FIXME
        Execute a gentle landing sequence directly downward from current position.
        
        Parameters
        ----------
        ground_z : float (optional) 
            Height to land at. (unit: m)
        decrement : int (optional)
            Distance between target keyframes. Defaults to 3. (unit: cm)
        timestep : float (optional)
            Time between target keyframes. Defaults to 0.15. (unit: s)

    `land_to_moving_target(self, target, z_offset=0.5, decrement=3, timestep=0.15)`
    :   FIXME: DO NOT USE. NOT SUITABLE FOR MULTIPLE DRONES.
        Execute a gentle landing sequence aiming at a live target.
        
        Parameters
        ----------
        target : object
            An object that has a pose attribute
        z_offset : float (optional)
            Vertical offset between target and landing start pose. (unit: m, default: 0.5)
        decrement : int (optional)
            Distance between target keyframes. (unit: cm, default: 3)
        timestep : float (optional
            Time between target keyframes. (unit: s, default: 0.15)

    `safe_position_setpoint(self, target, world=None)`
    :   Set a clean absolute position setpoint
        within safe airspace defined by world.
        
        Parameters
        ----------
        target : Pose
            Pose object bearting target coordinate and yaw.
            Yaw defaults to 0 if not supplied.
        world : World (optional)
            World object defining airspace rules.
            Defaults to object's own world if not supplied.

    `set_speed_limit(self, speed_limit)`
    :   Set speed limit.
        
        Parameters
        ----------
        speed_limit : float
            Limit for horizontal (xy) and vertical (z) speed. (unit: m/s)

    `setup(self)`
    :   Execute drone engineering boilerplate.
        Assumes most drone parameters at factory defaults.
        If in doubt, inspect drone parameters
        using Bitcraze client and documentation.