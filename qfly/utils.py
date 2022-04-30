import math
import sys
import threading
import traceback


def sqrt(x):
    """
    Calculate sqrt while avoiding rounding errors with slightly negative x.
    """
    if x < 0.0:
        return 0.0
    return math.sqrt(x)


def pol2cart(rho, phi):
    """
    Convert from polar (rho, phi) to cartesian (x, y) coordinates. phi is in degrees.
    """
    x = rho * math.cos(math.radians(phi))
    y = rho * math.sin(math.radians(phi))
    return(x, y)


def sph2cart(r, theta, phi):
    """
    Convert from spherical (rho, theta, phi) to cartesian (x, y, z) coordinates. 
    phi and theta in degrees.
    """
    x = r * math.sin(math.radians(theta)) * math.cos(math.radians(phi))
    y = r * math.sin(math.radians(theta)) * math.sin(math.radians(phi))
    z = r * math.cos(math.radians(theta))
    return(x, y, z)
