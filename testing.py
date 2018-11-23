#!/usr/bin/python
from time import localtime, mktime, sleep
import math
import sys


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

    def movement(self, **stations):
        current = mktime(localtime()) - mktime(self.time_start)
        y_LA = self.primary_x + current * self.velocity *\
            math.cos(math.atan(self.k)) / 3600
        x_LA = self.primary_y + current * self.velocity * \
            math.sin(math.atan(self.k)) / 3600 + self.b
        cords = dict(time=current, x_LA=x_LA, y_LA=y_LA)
        for key in stations:
            print(stations[key]['x_cords'])
#            k = (y_LA - y_cor)/(x_LA - x_cor)
#            b = y_cor - k*x_cor
#            if b >= 0:
#                equation = "%5.3fx+%5.3f" % (k, b)
#            if b < 0:
#                equation = "%5.3fx-%5.3f" % (k, abs(b))

        return cords


def input_stat(x_cordinates, y_cordinates, typeof, name):
        station = {
            "x_cords": x_cordinates,
            "y_cords": y_cordinates,
            "typeof": typeof,
            "name": name,
        }
        return station


if __name__ == "__main__":
    check = raw_input("Standart data? Y/n:")
    if check in 'Y yes y Yes ':
        stations = {'1': input_stat(x_cordinates=5,
                                    y_cordinates=5,
                                    typeof='radio',
                                    name='appolo_2000'
                                    )
                    }
        stations.update({'2': input_stat(x_cordinates=3,
                                         y_cordinates=4,
                                         typeof='radio',
                                         name='luna_1')})
        stations.update({'3': input_stat(x_cordinates=2,
                                         y_cordinates=6,
                                         typeof='radio',
                                         name='vladivostok'
                                         )
                         }
                        )
    else:
        for i in range(1, 4):
            print("Enter data for station %i" % i)
            x = input("x_cordinates:")
            y = input("y_cordinates:")
            t = input("type of station:")
            n = input("name of station:")
            stations = {'$i' % i: input_stat(x, y, t, n)}
    airplane = Plane(x_cord=0, y_cord=0, velocity=350, time=localtime(),
                     wireang=30, bank=35, pitch=30, k=1, b=0)
    myfile = open("output.txt", 'w')
    myfile.truncate()
    # Station_11 = Station(**station_1)
    myfile.write("time      x         y        equation\n")
    while(1):
        try:
            sleep(1)
            a = airplane.movement(**stations)
#            myfile.write('{:04.1f}'.format(a['time']) + "     " +
#                         '{:6.3f}'.format(a['x_LA']) + "    " +
#                         '{:6.3f}'.format(a['y_LA']) + "    " +
#                         a['equation'] + "\n")
            # print(a)
        except KeyboardInterrupt:
            print("======Pressed CTRL-C=======")
            myfile.close()
            sys.exit(0)
