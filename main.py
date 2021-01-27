import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QDoubleSpinBox, QSpinBox, QComboBox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from function import Data, Visualize

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.data = Data('data.csv')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('TEST PROGRAM')

        self.data_choose = QComboBox()
        d=self.data.get_data()
        self.data_choose.addItem(d.index)
        self.cal_button = QPushButton('Calculate')
        self.data_cell = QLabel('a')
        self.input_num = QSpinBox()
        self.input_num.setValue(1)
        self.input_num.valueChanged.connect(self.changeCellNum)
        self.input_cell_x = [QDoubleSpinBox()]
        self.input_cell_y = [QDoubleSpinBox()]
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.inputbox_x = QHBoxLayout()
        self.inputbox_y = QHBoxLayout()
        self.inputbox_xy = QVBoxLayout()
        self.inputbox = QHBoxLayout()
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        self.vbox.addWidget(self.data_cell)
        self.inputbox.addWidget(self.input_num)
        self.inputbox_x.addWidget(self.input_cell_x[0])
        self.inputbox_y.addWidget(self.input_cell_y[0])
        self.inputbox_xy.addLayout(self.inputbox_x)
        self.inputbox_xy.addLayout(self.inputbox_y)
        self.inputbox.addLayout(self.inputbox_xy)
        self.vbox.addLayout(self.inputbox)
        self.vbox.addWidget(self.cal_button)
        self.vbox.addWidget(self.canvas)
        self.hbox.addLayout(self.vbox)

        self.setLayout(self.hbox)


        self.showMaximized()

    def changeCellNum(self, num):
        current = len(self.input_cell_x)
        if num > current:
            for i in range(num-current):
                self.input_cell_x.append(QDoubleSpinBox())
                self.inputbox_x.addWidget(self.input_cell_x[-1])
                self.input_cell_y.append(QDoubleSpinBox())
                self.inputbox_y.addWidget(self.input_cell_y[-1])
        elif num < current:
            for i in range(current-num):
                self.inputbox_x.removeWidget(self.input_cell_x[-1])
                del self.input_cell_x[-1]
                self.inputbox_y.removeWidget(self.input_cell_y[-1])
                del self.input_cell_y[-1]







if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())