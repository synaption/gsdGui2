import cartopy.geodesic as gd
import numpy
from tdoa import *
import datetime
import dateutil.parser
from sympy import sin, cos
from collections import namedtuple
import math
from problem_of_apollonius import *


def geo(combination):
    #print(combination)
    pi1 = combination[0]
    pi2 = combination[1]
    pi3 = combination[2]
    cd1 = numpy.array([pi1['longitude'], pi1['latitude']]) 
    cd2 = numpy.array([pi2['longitude'], pi2['latitude']]) 
    cd3 = numpy.array([pi3['longitude'], pi3['latitude']]) 
    #cx = numpy.array([29.9610375, -90.0634532]) #known location
    cx = numpy.array([-90.0636178, 29.9610882]) #known location / origen
    #cx = numpy.array([-90.0624654 , 29.9638835])
    #cx = numpy.array([29.9638835 , -90.0624654])
    
    first_impulse_time =  pi1['onset_time']
    second_impulse_time = pi2['onset_time']
    third_impulse_time =  pi3['onset_time']
    
    #print(first_impulse_time, second_impulse_time, third_impulse_time)
    
    k = gd.Geodesic() #defaults to WGS84
    rtwo = 343 * tdoa(first_impulse_time, second_impulse_time)#k.inverse(c1, c4).base[0,0] - k.inverse(c1, c3).base[0,0]
    rtwo = round(rtwo,2) 
    rthree = 343 * tdoa(first_impulse_time, third_impulse_time)#k.inverse(c6, c1).base[0,0] - k.inverse(c1, c3).base[0,0]
    rthree = round(rthree, 2)
    rone_dict = {'r': 0}
    pi1.update(rone_dict)
    rtwo_dict = {'r': float(rtwo)}
    pi2.update(rtwo_dict)
    print(rtwo_dict)
    rthree_dict = {'r': float(rthree)}
    pi3.update(rthree_dict)
    print(rthree_dict)

    
    cir1x, cir1y = convert2xy(cd1, cx)
    cir2x, cir2y = convert2xy(cd2, cx)
    cir3x, cir3y = convert2xy(cd3, cx)
    c1, c2, c3 = Circle(cir1x, cir1y, 1), Circle(cir2x, cir2y, rtwo), Circle(cir3x, cir3y, rthree)
    circ4 = solveApollonius(c1, c2, c3, -1, -1, -1)
    x, y, rone = circ4 
    print(circ4)
    sourcelon, sourcelat, offby = convert2coordinates(x, y, cx)
    print(offby)
    return rone, rtwo, rthree, sourcelat, sourcelon, pi1['event_id'], offby
    

