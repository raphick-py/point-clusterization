#!/usr/bin/python
from time import localtime, mktime, sleep
import math
import sys
import numpy as np
import random
#class Station(object):
#
#    def __init__(self, **kwargs):
#        for key in kwargs:
#            if key == "x_cords":
#                self.cords_x = kwargs[key]
#            if key == "y_cords":
#                self.cords_y = kwargs[key]
#            if key == "type":
#                self.typeof = kwargs[key]
#            if key == "name":
#                self.names = kwargs[key]
#            if key == "wave_distance":
#                self.distance = kwargs[key]
#            if key == "operation_mode":
#                self.operation_mode = kwargs[key]


class Plane(object):

    def __init__(self, **kwargs):
        '''Class for LA object'''
        for key in kwargs:
            if key == 'x_cord':
                self.primary_x = kwargs[key]
            if key == 'y_cord':
                self.primary_y = kwargs[key]
            if key == 'velocity':
                self.velocity = kwargs[key]
            if key == 'time':
                self.time_start = kwargs[key]
            if key == 'wireang':
                self.wire_angle = kwargs[key]
            if key == 'banl':
                self.bank = kwargs[key]
            if key == 'pitch':
                self.pitch = kwargs[key]
            if key == 'k':
                self.k = kwargs[key]
            if key == 'b':
                self.b = kwargs[key]

    def movement(self, t, **stations):
        '''calculation of LA movemnt and build of equation of station to LA'''
        current = t
        y_LA = self.primary_x + current * self.velocity *\
            math.cos(math.atan(self.k)) / 3600
        x_LA = self.primary_y + current * self.velocity * \
            math.sin(math.atan(self.k)) / 3600 + self.b
        cords = dict(time=current, x_LA=x_LA, y_LA=y_LA,)
        for key in stations:
            k = (y_LA - stations[key]['y_cords']) / \
                (x_LA - stations[key]['x_cords'])
            delt = random.normalvariate(0, 40)
            delt_rad = (math.pi / 180) * delt
            k = math.tan(math.atan(k) + delt_rad)
            b = stations[key]['y_cords'] - k*stations[key]['x_cords']
            delt = random.normalvariate(0, 0.5)
            b = b + delt
            if b >= 0:
                equation = "%5.3fx+%5.3f" % (k, b)
            if b < 0:
                equation = "%5.3fx-%5.3f" % (k, abs(b))
            cords.update({'equation_%s' % key: equation,
                          'k_%s' % key: k,
                          'b_%s' % key: b
                          }
                         )
        return cords


def input_stat(x_cordinates, y_cordinates, typeof, name):
        station = {
            "x_cords": x_cordinates,
            "y_cords": y_cordinates,
            "typeof": typeof,
            "name": name,
        }
        return station


def stationsd():
    check = input("Standart data? Y/n:")
    if check in 'Y yes y Yes ':
        stations = {'1': input_stat(x_cordinates=2,
                                    y_cordinates=9,
                                    typeof='radio',
                                    name='appolo_2000'
                                    )
                    }
        stations.update({'2': input_stat(x_cordinates=9,
                                         y_cordinates=2,
                                         typeof='radio',
                                         name='luna_1')})
        stations.update({'3': input_stat(x_cordinates=8,
                                         y_cordinates=4,
                                         typeof='radio',
                                         name='vladivostok'
                                         )
                         }
                        )
    else:
        for i in range(1, 4):
            print("Enter data for station %i" % i)
            x = float(input("x_cordinates:"))
            y = float(input("y_cordinates:"))
            t = str(input("type of station:"))
            n = str(input("name of station:"))
            stations = {"$i" % i: input_stat(x, y, t, n)}
    return stations


def creation_sys_cords(step):
    p = []
    i = 0
    while(i < 9.9):
        p.append(round(i, 3))
        i += step
    return np.array(p)


def for_draw(stations):
    LA = Plane(x_cord=0, y_cord=0, velocity=350, time=localtime(),
               wireang=30, bank=35, pitch=30, k=1, b=0)
    q = 0
    x = creation_sys_cords(0.01)
    d = {}
    while(q < 140):
        a = LA.movement(q, **stations)
        y_1 = float(a['k_1']) * x + float(a['b_1'])
        y_2 = float(a['k_2']) * x + float(a['b_2'])
        y_3 = float(a['k_3']) * x + float(a['b_3'])
        m = {'y1': y_1, 'y2': y_2, 'y3': y_3}
        d.update({'t=%i' % q: m})
        q += 1
    return d


if __name__ == "__main__":
    stations = stationsd()
    airplane = Plane(x_cord=0, y_cord=0, velocity=350, time=localtime(),
                     wireang=30, bank=35, pitch=30, k=1, b=0)
    myfile = open("output.txt", 'w')
    myfile.truncate()
    myfile.write("time      x         y        equations\n")
    i = 0
    while(i < 50):
        try:
            a = airplane.movement(i, **stations)
            myfile.write('{:04.1f}'.format(a['time']) + "     " +
                         '{:6.3f}'.format(a['x_LA']) + "    " +
                         '{:6.3f}'.format(a['y_LA']) + "    " +
                         a['equation_1'] + '    ' +
                         a['equation_2'] + '    ' +
                         a['equation_3'] + "\n")
            i += 1
        except KeyboardInterrupt:
            print("======Pressed CTRL-C=======")
            myfile.close()
            sys.exit(0)
    myfile.close()
