"""
qfly | Qualisys Drone SDK is a Python library to track and fly drones with
Qualisys motion capture systems. It is is designed to be an entry point for 
students, researchers, engineers, artists, and designers to develop drone 
applications.

.. include:: ../README.md
"""


from .crazyflie import QualisysCrazyflie
from .pose import Pose
from .qtm_wrapper import QtmWrapper
from .world import World
from .parallel import parallel
