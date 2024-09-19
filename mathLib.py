from numpy import array
from math import trunc, sin, cos, pi

def lerp(a, b, alpha):
    if isinstance(a,list) :
        if len(a) != len(b) : return -1
        if len(a) == 0 or len(b) == 0 : return -1
        output = []
        for x in range(len(a)):
            output.append((alpha * (b[x] - a[x])) + a[x])
        return output
    
    return (alpha * (b - a)) + a

def rotate_point(xy: array, degrees):
    theta = degrees * pi
    return array([
        trunc(xy[0]*cos(theta)-xy[1]*sin(theta)),
        trunc(xy[1]*cos(theta)+xy[0]*sin(theta))
    ])