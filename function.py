import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Data:
    def __init__(self, filename):
      self.data = pd.read_csv(filename,header = 0)
      self.data=self.data.set_index(['Name', 'CONDITION'])
    def __str__(self):
      return str(self.data)
    def show_data(self,num=None):
      self.data.head(num)
    def get_data(self):
      return self.data
    def get_listdata(self,index, condition):
      d = pd.DataFrame(self.data.loc[index].loc[condition])
      point_x = []
      point_y = []
      for i in range(len(d)//2):
        point_x.append('Point'+str (i+1)+'x')
        point_y.append('Point'+str (i+1)+'y')
      data_x = d.loc[point_x]
      data_y = d.loc[point_y]
      return data_x.values.tolist(), data_y.values.tolist()


class Visualize:
  def __init__(self, ax, data):
    self.ax = ax
    self.data = data
    self.x_data_list = []
    self.y_data_list = []
    self.count = 0
    self.title = '51GS'
    self.data_i = data.get_data().index[0][0]
    self.condition = self.data.get_data().loc[self.data_i].index.values[0]


  def draw(self):
    self.ax.set_title(self.title)
    self.ax.plot(self.x_data_list[-1], self.y_data_list[-1])
    return self.ax
  
  def draw_data(self):
    self.ax.set_title(self.title)
    x, y = self.data.get_listdata(self.data_i, self.condition)
    self.ax.plot(x, y)
    self.ax.grid(True, color='gray')
    self.ax.set_xlabel('current\n'+self.condition)
    self.ax.set_ylabel('second')
    return self.ax

  
  def addData(self, x_data, y_data):
    self.x_data_list.append(x_data)
    self.y_data_list.append(y_data)

  def changeData(self, index):
    self.data_i = index
    self.title = index
    self.condition = self.data.get_data().loc[self.data_i].index.values[0]
    self.ax=self.draw_data()
    return self.ax
  def clear(self):
    plt.close()
  def changeCondition(self, condition):
    self.condition = condition
    self.ax = self.draw_data()
    return self.ax


  
  def calError(self):
    data_x, data_y = self.data.get_listdata(self.data_i, self.condition)
    in_x = self.x_data_list[-1]
    in_y = self.y_data_list[-1]
    error = -1
    for i in range(len(data_x)):
      for j in range(len(in_x)):
        if data_x[i][0] == in_x[j]:
          error=max((np.abs(data_y[i][0]-in_y[j]))/data_y[i][0],error)
    return error
  
  def set_title(self, MAX_ERROR=5/100, error=0):
    if error < 0:
      self.title = "don't have same xpoint"
    elif MAX_ERROR > error:
      self.title = self.data_i+' good, error: {}%'.format(error * 100)
    else:
      self.title = self.data_i+' fail, error: {}%'.format(error*100)
