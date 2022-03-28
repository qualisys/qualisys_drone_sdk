import math

def sqrt(x):
    """Calculate sqrt while avoiding rounding errors with slightly negative x."""
    if x < 0.0:
        return 0.0
    return math.sqrt(x)

class Object(object):
    pass