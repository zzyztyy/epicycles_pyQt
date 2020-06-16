import numpy as np


class Epi(object):
    def __init__(self, points):
        self.points = points
        self.circles = list()

    def solve(self, by='radius'):
        z = [x+y*1j for x, y in self.points]
        z = np.fft.fft(z)
        len_z = len(z)
        for i in range(len_z):
            r = abs(z[i] / len_z)
            p = np.arctan2(z[i].imag, z[i].real)
            omg = [i, i-len_z][i > len_z/2]
            self.circles.append((r, omg, p))
        self.sort_circles(by)

    def sort_circles(self, by='radius'):
        if by == 'radius':
            self.circles = sorted(self.circles, key=lambda b: -b[0])
        elif by == 'fre':
            self.circles = sorted(self.circles, key=lambda b: abs(b[1]))
