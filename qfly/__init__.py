#
#  "qfly"
#  Qualisys Drone SDK
#
#  Copyright (C) 2022 Qualisys AB
#

# include README to auto-generate documentation with pdoc
"""
.. include:: ../README.md
"""


from .crazyflie import QualisysCrazyflie
from .deck import QualisysDeck
from .pose import Pose
from .qtm import QtmWrapper
from .traqr import QualisysTraqr
from .world import World
from .parallel_contexts import ParallelContexts