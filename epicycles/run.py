from PyQt5.QtWidgets import QMainWindow, QLabel, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot

from epicycles.mainWindowUI import Ui_MainWindow
from epicycles.figure import Figure
from epicycles.epi import Epi


author = 'zzyztyy & sclereid'
github = 'https://github.com/sclereid/epicycles'
connect = 'Connect the Author\n zzyztyy & sclerid in GitHub or\n by Email 2375672032@qq.com'


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.canvas = Figure(self.frame, width=self.frame.width(), height=self.frame.height())
        self.label_5 = PicLabel(self)
        preview_map = QtGui.QPixmap('resource/default.png').scaled(
            self.previewLabel.width(), self.previewLabel.height())
        self.setWindowIcon(QtGui.QIcon('resource/icon.ico'))
        self.previewLabel.setPixmap(preview_map)

        self.sorted_by = 'radius'
        self.inFrame = True
        self.x, self.y = 0, 0
        self.points, self.circles = list(), list()

        self.set_connect()

    def set_connect(self):
        self.solveButton.clicked.connect(self.solve_fft)
        self.runButton.clicked.connect(self.draw_circles)
        self.backButton.clicked.connect(self.back)
        self.clearButton.clicked.connect(self.clear)

        self.fpsSlider.sliderMoved.connect(self.change_fps)
        self.duraSlider.sliderMoved.connect(self.change_duration)
        self.interSlider.sliderMoved.connect(self.change_inter)
        self.resolSlider.sliderMoved.connect(self.change_resolution)

        self.raidusButton.clicked.connect(self.change_sorted_by)
        self.freButton.clicked.connect(self.change_sorted_by)

        self.actionRun.triggered.connect(self.draw_circles)
        self.actionClear.triggered.connect(self.clear)
        self.actionExit.triggered.connect(self.close)

        self.actionopen_Image.triggered.connect(self.open_image)
        self.actionclose_image.triggered.connect(self.close_image)
        self.actionrefresh.triggered.connect(self.refresh)

        self.action_gif.triggered.connect(self.save_gif)

        self.actionGitHub.triggered.connect(self.open_github)
        self.actionAbout.triggered.connect(self.response_about)

    @pyqtSlot()
    def solve_fft(self):
        epi = Epi(self.points)
        epi.solve(self.sorted_by)
        self.circles = epi.circles
        self.canvas.build_path(self.circles)
        preview_map = QtGui.QPixmap('resource/pre.png')
        self.previewLabel.setPixmap(preview_map)
        self.runButton.setEnabled(True)
        self.actionRun.setEnabled(True)

    @pyqtSlot()
    def draw_circles(self):
        self.canvas.restart()
        self.canvas.draw_circle(self.circles)
        self.canvas.show_points(self.points)
        self.canvas.draw()

    @pyqtSlot()
    def back(self):
        self.runButton.setEnabled(False)
        self.actionRun.setEnabled(False)
        if self.points:
            self.points.pop()
        if not self.points:
            self.backButton.setEnabled(False)
            self.solveButton.setEnabled(False)
        self.canvas.restart()
        self.canvas.show_points(self.points)
        self.canvas.draw()

    @pyqtSlot()
    def clear(self):
        self.runButton.setEnabled(False)
        self.actionRun.setEnabled(False)
        self.backButton.setEnabled(False)
        self.solveButton.setEnabled(False)
        self.points.clear()
        self.canvas.restart()
        self.canvas.show_points(self.points)
        self.canvas.draw()

    @pyqtSlot()
    def change_fps(self):
        fps = self.fpsSlider.value()*10
        self.canvas.set_fps(fps)
        self.fpsLabel.setText(str(fps)+' FPS')

    @pyqtSlot()
    def change_duration(self):
        dura = self.duraSlider.value()
        self.canvas.set_duration(dura)
        self.durationLabel.setText(str(dura)+'s duration')

    @pyqtSlot()
    def change_inter(self):
        inter = self.interSlider.value()
        self.canvas.set_inter(inter)
        self.interLabel.setText(str(inter)+' interpolate')

    @pyqtSlot()
    def change_resolution(self):
        resol = 2**self.resolSlider.value()
        self.canvas.set_resol(resol)
        self.resoLabel.setText(str(resol)+' resolution')

    @pyqtSlot()
    def change_sorted_by(self):
        self.sorted_by = ['fre', 'radius'][self.raidusButton.isChecked()]
        epi = Epi(self.points)
        epi.solve(self.sorted_by)
        self.circles = epi.circles
        self.draw_circles()

    @pyqtSlot()
    def save_gif(self):
        self.canvas.save('gif')

    @pyqtSlot()
    def open_image(self):
        file_name, file_type = QFileDialog.getOpenFileName(
            self, "chose file", "./", "*.jpg *.png;;All Files(*)")
        self.canvas.set_back_pic(file_name)
        self.canvas.restart()
        self.canvas.show_points(self.points)
        self.canvas.draw()

    @pyqtSlot()
    def close_image(self):
        self.canvas.remove_back_pic()
        self.canvas.restart()
        self.canvas.show_points(self.points)
        self.canvas.draw()

    @pyqtSlot()
    def refresh(self):
        self.canvas.restart()
        self.canvas.draw_circle(self.circles)
        self.canvas.show_points(self.points)
        self.canvas.draw()

    @pyqtSlot()
    def open_github(self):
        QtGui.QDesktopServices.openUrl(QUrl(github))

    @pyqtSlot()
    def response_about(self):
        QMessageBox.about(self, 'About', connect)


class PicLabel(QLabel):
    def __init__(self, parent=None):
        super(PicLabel, self).__init__(parent)
        self.parent = parent
        self.frame = parent.frame
        self.canvas = self.parent.canvas
        self.pic_x, self.pic_y = 0, 0
        self.x0, self.y0 = self.frame.x(), self.frame.y()+self.parent.menubar.height()
        self.start_up()

    def start_up(self):
        if self.parent:
            self.setGeometry(self.x0, self.y0, self.frame.width(), self.frame.height())
        self.setMouseTracking(True)

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent) -> None:
        w, h = self.frame.width(), self.frame.height()
        self.pic_x, self.pic_y = ev.x() - self.x() + self.x0, ev.y() - self.y() + self.y0
        if 0 < self.pic_x < w and 0 < self.pic_y < h:
            self.parent.inFrame = True
            self.parent.statusbar.showMessage('x=' + str(self.pic_x - w // 2) + ' y=' + str(self.pic_y - h // 2), 2000)
            self.update()
        else:
            self.parent.inFrame = False

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter()
        painter.begin(self)
        pen = QtGui.QPen(Qt.black, 1, Qt.DashLine)
        painter.setPen(pen)
        painter.drawLine(self.pic_x, self.y()-self.y0, self.pic_x, self.height()+self.y()-self.y0)
        painter.drawLine(self.x()-self.x0, self.pic_y+self.y()-self.y0,
                         self.x()+self.width()-self.x0, self.pic_y+self.y()-self.y0)
        painter.end()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            if self.parent.inFrame:
                x, y = a0.x(), self.frame.height()-a0.y()
                self.parent.points.append((x, y))
                self.parent.solveButton.setEnabled(True)
                self.parent.runButton.setEnabled(False)
                self.parent.actionRun.setEnabled(False)
                if self.parent.points:
                    self.parent.backButton.setEnabled(True)
                else:
                    self.parent.backButton.setEnabled(False)
                self.canvas.restart()
                self.canvas.show_points(self.parent.points)
                self.canvas.draw()
        elif a0.button() == Qt.RightButton:
            self.parent.refresh()
