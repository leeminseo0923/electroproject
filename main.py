import sys
from PyQt5.QtCore import QAbstractAnimation
from PyQt5.QtWidgets import QAbstractItemView, QWidget, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QDoubleSpinBox, QSpinBox, QComboBox, QTableWidget, QTableWidgetItem
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from function import Data, Visualize

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.data = Data('data.csv')
        self.parameters = {'axes.labelsize' : 20, 'axes.titlesize':25}
        plt.rcParams.update(self.parameters)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('TEST PROGRAM')

        self.data_choose = QComboBox()
        d=self.data.get_data()
        for i in range(len(d)):
            if d.index[i][0] != self.data_choose.itemText(i-1):
                self.data_choose.addItem(d.index[i][0])
        self.data_choose.activated[str].connect(self.onActivated)

        self.data_condition = QComboBox()
        dc = d.loc[d.index[0][0]]
        for i in range(len(dc)):
            self.data_condition.addItem(dc.index.values[i])
        self.data_condition.activated[str].connect(self.onActivated_condition)

        self.fig, self.ax = plt.subplots(figsize=(50,100))
        self.vis = Visualize(self.ax, self.data)
        self.canvas = FigureCanvas(self.fig)
        self.cal_button = QPushButton('Calculate')
        self.cal_button.clicked.connect(self.calculate)
        self.clr_button = QPushButton('Clear')
        self.clr_button.clicked.connect(self.clear)
        tempx, tempy = self.data.get_listdata(d.index[0][0], dc.index.values[0])
        self.data_cell = QTableWidget()
        self.data_cell.setColumnCount(7)
        self.data_cell.setRowCount(2)
        self.data_cell.setMaximumHeight(100)
        self.data_cell.setHorizontalHeaderLabels(['Point1','Point2','Point3','Point4','Point5','Point6','Point7'])
        self.data_cell.setVerticalHeaderLabels(['x','y'])
        self.graph_print = QPushButton('Print')
        self.graph_print.clicked.connect(self.print_graph)
        for idx ,item in enumerate(tempx):
            self.data_cell.setItem(0,idx,QTableWidgetItem(str(item[0])))
        for idx, item in enumerate(tempy):
            self.data_cell.setItem(1, idx, QTableWidgetItem(str(item[0])))
        self.data_cell.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
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
        self.btnbox.addWidget(self.graph_print)
        self.vbox.addWidget(self.data_choose)
        self.vbox.addWidget(self.data_condition)
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
        self.ax = self.vis.draw_data()
        self.canvas.draw()
    def onActivated(self, text):
        plt.cla()
        self.ax=self.vis.changeData(text)
        self.canvas.draw()
        self.data_condition.clear()
        d = self.data.get_data()
        d = d.loc[text]
        for item in d.index.values:
            self.data_condition.addItem(item)
        self.change_cell(text, self.vis.condition)
    
    def change_cell(self, name, condition):
        self.data_cell.clear()
        x, y = self.data.get_listdata(name, condition)
        for idx ,item in enumerate(x):
            self.data_cell.setItem(0,idx,QTableWidgetItem(str(item[0])))
        for idx, item in enumerate(y):
            self.data_cell.setItem(1, idx, QTableWidgetItem(str(item[0])))

    
    def print_graph(self):
        self.canvas.print_png('test.png')
    
    def onActivated_condition(self, text):
        plt.cla()
        self.ax = self.vis.changeCondition(text)
        self.canvas.draw()
        self.change_cell(self.vis.data_i, text)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())