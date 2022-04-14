import math


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
