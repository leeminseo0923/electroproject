import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Data:
    def __init__(self, filename):
      self.data = pd.read_csv(filename,header = 0)
      self.data=self.data.set_index('Name')
    def __str__(self):
      return str(self.data)
    def show_data(self,num=None):
      self.data.head(num)
    def get_data(self):
      return self.data
    def get_listdata(self,index):
      d = self.data.loc[[index]]
      point_x = []
      point_y = []
      for i in range(len(d.columns)//2):
        point_x.append('Point'+str (i+1)+'x')
        point_y.append('Point'+str (i+1)+'y')
      data_x = d[point_x]
      data_y = d[point_y]
      return data_x.values.tolist()[0], data_y.values.tolist()[0]


class Visualize:
  def __init__(self, ax, data):
    self.ax = ax
    self.data = data
    self.x_data_list = []
    self.y_data_list = []
    self.count = 0
    self.title = 'EMPTY INPUT'
    self.data_i = data.get_data().index[0]


  def draw(self):
    self.ax.set_title(self.title)
    self.ax.plot(self.x_data_list[-1], self.y_data_list[-1])
    return self.ax
  
  def draw_data(self):
    self.ax.set_title(self.title)
    x, y = self.data.get_listdata(self.data_i)
    self.ax.plot(x, y)
    self.ax.grid(True, color='gray')
    self.ax.set_xlabel('a')
    self.ax.set_ylabel('s')
    return self.ax

  
  def addData(self, x_data, y_data):
    self.x_data_list.append(x_data)
    self.y_data_list.append(y_data)

  def changeData(self, index):
    self.data_i = index
    self.ax=self.draw_data()
    return self.ax
  def clear(self):
    plt.close()


  
  def calError(self):
    data_x, data_y = self.data.get_listdata(self.data_i)
    in_x = self.x_data_list[-1]
    in_y = self.y_data_list[-1]
    error = -1
    for i in range(len(data_x)):
      for j in range(len(in_x)):
        if data_x[i] == in_x[j]:
          error=max((np.abs(data_y[i]-in_y[j]))/data_y[i],error)
          print(error)
    return error
  
  def set_title(self, MAX_ERROR=5/100, error=0):
    if error < 0:
      self.title = "don't have same xpoint"
    elif MAX_ERROR > error:
      self.title = 'good, error: {}%'.format(error * 100)
    else:
      self.title = 'fail, error: {}%'.format(error*100)
