import math


def sqrt(x):
    """
    Calculate sqrt while avoiding rounding errors with slightly negative x.

    Parameters
    ----------
    x : float
        Number to calculate square root of.
    """
    if x < 0.0:
        return 0.0
    return math.sqrt(x)


def pol2cart(r, phi):
    """
    Convert from polar (rho, phi)
    to cartesian (x, y) coordinates.

    Parameters
    ----------
    r : float
        Radial distance to origin.
        (Unit: m)
    phi : float
        Azimuthal angle.
        (Unit: degrees)
    """
    x = r * math.cos(math.radians(phi))
    y = r * math.sin(math.radians(phi))
    return(x, y)


def sph2cart(r, theta, phi):
    """
    Convert from spherical (rho, theta, phi)
    to cartesian (x, y, z) coordinates.

    Parameters
    ----------
    r : float
        Radial distance to origin.
        (Unit: m)
    theta : float
        Polar angle.
        (Unit: degrees)
    phi : float
        Azimuthal angle.
        (Unit: degrees)
    """
    x = r * math.sin(math.radians(theta)) * math.cos(math.radians(phi))
    y = r * math.sin(math.radians(theta)) * math.sin(math.radians(phi))
    z = r * math.cos(math.radians(theta))
    return(x, y, z)
