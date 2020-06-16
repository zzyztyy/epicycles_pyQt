# coding:utf-8

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.animation as animation
import matplotlib.image as im
import numpy as np
from PyQt5 import QtWidgets

import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')
PI = 3.14159265357


class Figure(FigureCanvas):
    def __init__(self, parent=None, width=500, height=400, dpi=100, fps=30, duration=10):
        self.w, self.h, = width, height
        self.fig = plt.figure(figsize=((width-1)/dpi, (height-1)/dpi), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.back_alpha = 1
        self.ani = None
        self.img = None
        self.pages, self.inter = int(24*duration), 1000/fps
        self.inter, self.resolution = 5, 0.25
        self.restart()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def set_fps(self, fps):
        self.inter = 1000/fps

    def set_duration(self, duration):
        self.pages = 24*duration

    def set_resol(self, resol):
        self.resolution = resol

    def set_inter(self, inter):
        self.inter = inter

    def restart(self):
        self.axes.cla()
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.axes.set_xlim(0, 600)
        self.axes.set_ylim(0, 600)
        self.axes.set_facecolor('beige')
        self.back_alpha = 1
        if self.img is not None:
            self.axes.imshow(self.img)

    def show_points(self, points):
        if points:
            xs, ys = [p[0] for p in points], [p[1] for p in points]
            self.axes.scatter(xs, ys, edgecolor='r', c='', alpha=self.back_alpha)
            self.axes.plot(xs+[xs[0]], ys+[ys[0]], c='grey', lw=1, alpha=self.back_alpha)
        else:
            self.axes.plot([], [])

    def draw_circle(self, circles):
        min_circle = self.resolution
        self.back_alpha = 0.25
        ax = self.axes
        t_all = 100
        t = np.linspace(0, 1, t_all)
        times = np.linspace(0, 1, self.pages)

        def update_pic(page):
            time = times[page]
            cxu, cyu = [], []
            x0u, y0u = 0, 0
            for circleu in circles:
                ru, wu, pu = circleu
                if ru > min_circle:
                    wu = wu * PI * 2
                    cxu = cxu + [float('nan')] + [x0u] * t_all
                    cyu = cyu + [float('nan')] + [y0u] * t_all
                    x0u, y0u = x0u + ru * np.cos(pu + wu * time), y0u + ru * np.sin(pu + wu * time)
            line_ani.set_data(np.array(x)+np.array(cxu), np.array(y)+np.array(cyu))
            point_ani.set_data(cxu[1::100], cyu[1::100])

            path_ani.set_data(target_x[:page+1], target_y[:page+1])
            target_ani.set_data(target_x[page], target_y[page])
            return line_ani, point_ani, target_ani

        target_x, target_y = np.zeros(self.pages), np.zeros(self.pages)
        cx, cy = [], []
        x, y = [], []
        for circle in circles:
            r, w, p = circle
            if r > min_circle:
                w = w*PI*2
                cx = cx + [float('nan')] + [target_x[-1]] * t_all
                cy = cy + [float('nan')] + [target_y[-1]] * t_all
                x = x + [float('nan')] + list(r * np.cos(w*t+p))
                y = y + [float('nan')] + list(r * np.sin(w*t+p))
                # target_x, target_y = target_x + r * np.cos(p), target_y + r * np.sin(p)
                target_x, target_y = target_x + r * np.cos(p + w * times), target_y + r * np.sin(p + w * times)

        circles_x, circles_y = np.array(cx)+np.array(x), np.array(cy)+np.array(y)
        line_ani, = ax.plot(circles_x, circles_y, lw=1, c='c')
        point_ani, = ax.plot(cx[::100], cy[::100], c='c', marker='o', ls='', markersize='2')
        path_ani, = ax.plot(target_x[:0], target_y[:0], color='b', ls='--', lw=1)
        target_ani, = ax.plot(target_x[0], target_y[0], 'ro')

        self.ani = animation.FuncAnimation(self.fig, update_pic, frames=self.pages, interval=self.inter)

    def build_path(self, circles, width=200, height=200, dpi=100):
        fig = plt.figure(figsize=[width/dpi, height/dpi], dpi=dpi)
        ax = fig.add_subplot(111, frameon=False)
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        # ax.set_xlim(0, 600)
        # ax.set_ylim(0, 600)
        # fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        time = np.linspace(0, 1, self.pages)
        x0, y0 = np.zeros(self.pages), np.zeros(self.pages)
        for circle in circles:
            r, w, p = circle
            w = w * PI * 2
            x0, y0 = x0 + r * np.cos(p+w*time), y0 + r * np.sin(p+w*time)
        ax.plot(x0, y0, lw=1)
        fig.savefig('resource/pre.png')
        fig.show()
        plt.close()

    def set_back_pic(self, image):
        img = im.imread(image)
        self.img = self.resize_pic(img)

    @staticmethod
    def resize_pic(img):
        w, h, c = np.shape(img)
        w2, h2 = 600, 600
        max_value = np.max(img)
        if max_value > 1:
            default_color = {1: 1, 3: [191, 191, 191], 4: [191, 191, 191, 0.]}
            img2 = np.ones([w2, h2, c], dtype=int)
        else:
            default_color = {1: 1, 3: [0.75, 0.75, 0.75], 4: [0.75, 0.75, 0.75, 1.]}
            img2 = np.ones([w2, h2, c], dtype=float)
        a, b = max(w, h), min(w2, h2)
        for x in range(w2):
            for y in range(h2):
                xt, yt = w//2-a*(x-300)//b, h//2+a*(y-300)//b
                if 0 <= xt < w and 0 <= yt < h:
                    img2[x][y] = img[xt][yt]
                else:
                    img2[x][y] = default_color[c]
        return img2

    def remove_back_pic(self):
        self.img = None

    def save(self, file_type='gif'):
        if self.ani:
            if file_type == 'gif':
                self.ani.save('ani.gif')
