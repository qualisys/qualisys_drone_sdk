Module qfly.qtm_wrapper
=======================

Classes
-------

`QtmWrapper(body, on_pose, qtm_ip='127.0.0.1')`
:   Wrapper for opening and running an asynchronous QTM connection
    that receives and responds to real time data packets.
    
    Designed for real time interactive applications, e.g. drone control.
    Each entity being tracked should:
    1) instantiate its own QtmWrapper,
    2) be defined as a rigid body in QTM,
    3) pass a callback function to its QtmWrapper which responds to pose data.
    
    Attributes
    ----------
    body : string
        name of rigid body being tracked
    on_pose: function
        callback to trigger when packet with pose is received
    qtm_ip : string
        IP address of QTM instance
    
    Construct QtmWrapper object
    
    Parameters
    ----------
    body : string
        Name of 6DOF rigid body being tracked
    on_pose : function(Pose)
        Callback to trigger when pose packet is received
    qtm_ip : string
        IP address of QTM instance

    ### Ancestors (in MRO)

    * threading.Thread

    ### Methods

    `close(self)`
    :   Stop QTM wrapper thread.

    `run(self)`
    :   Run QTM wrapper coroutine