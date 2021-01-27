import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QDoubleSpinBox, QSpinBox, QComboBox, QTableWidget, QTableWidgetItem
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
        for i in range(len(d)):
            self.data_choose.addItem(d.index[i])
        self.data_choose.activated[str].connect(self.onActivated)

        self.fig, self.ax = plt.subplots()
        self.vis = Visualize(self.ax, self.data)
        self.canvas = FigureCanvas(self.fig)
        self.cal_button = QPushButton('Calculate')
        self.cal_button.clicked.connect(self.calculate)
        self.clr_button = QPushButton('Clear')
        self.clr_button.clicked.connect(self.clear)
        tempx, tempy = self.data.get_listdata(d.index[0])
        self.data_cell = QTableWidget()
        self.data_cell.setColumnCount(10)
        self.data_cell.setRowCount(2)
        self.data_cell.setMaximumHeight(100)
        self.data_cell.setHorizontalHeaderLabels(['Point1','Point2','Point3','Point4','Point5','Point6','Point7','Point8','Point9','Point10'])
        self.data_cell.setVerticalHeaderLabels(['x','y'])
        for idx ,item in enumerate(tempx):
            self.data_cell.setItem(0,idx,QTableWidgetItem(str(item)))
        for idx, item in enumerate(tempy):
            self.data_cell.setItem(1, idx, QTableWidgetItem(str(item)))
        
        self.input_num = QSpinBox()
        self.input_num.setMaximumWidth(100)
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
        self.btnbox = QHBoxLayout()

        self.btnbox.addWidget(self.cal_button)
        self.btnbox.addWidget(self.clr_button)
        self.vbox.addWidget(self.data_choose)
        self.vbox.addWidget(self.data_cell)
        self.inputbox.addWidget(self.input_num)
        self.inputbox_x.addWidget(self.input_cell_x[0])
        self.inputbox_y.addWidget(self.input_cell_y[0])
        self.inputbox_xy.addLayout(self.inputbox_x)
        self.inputbox_xy.addLayout(self.inputbox_y)
        self.inputbox.addLayout(self.inputbox_xy)
        self.vbox.addLayout(self.inputbox)
        self.vbox.addLayout(self.btnbox)
        self.vbox.addWidget(self.canvas)
        self.hbox.addLayout(self.vbox)
        self.ax = self.vis.draw_data()
        self.canvas.draw()

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
    
    def calculate(self):
        in_x, in_y = [], []
        for item in self.input_cell_x:
            in_x.append(item.value())
        for item in self.input_cell_y:
            in_y.append(item.value())
        self.vis.addData(in_x, in_y)
        e=self.vis.calError()
        self.vis.set_title(5/100, e)
        self.ax = self.vis.draw()
        self.canvas.draw()
    def clear(self):
        plt.cla()
        # self.vis.clear()
        self.vis.title='EMPTY INPUT'
        self.ax = self.vis.draw_data()
        self.canvas.draw()
    def onActivated(self, text):
        plt.cla()
        # self.vis.clear()
        self.vis.title='EMPTY INPUT'
        self.ax=self.vis.changeData(text)
        self.canvas.draw()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())