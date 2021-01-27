import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Data:
    def __init__(self, filename):
      self.data = pd.read_csv(filename,header = 0)
      self.data.set_index('Name')

      point_x = []
      point_y = []

      for i in range(len(self.data.columns)//2):
        point_x.append('Point'+str (i+1)+'x')
        point_y.append('Point'+str (i+1)+'y')
      self.data_x = self.data[point_x].values.tolist()
      self.data_y = self.data[point_y].values.tolist()
    def __str__(self):
      return str(self.data)
    def show_data(self,num=None):
      self.data.head(num)
    def get_data(self):
      return self.data_x, self.data_y

      
filename = 'data.csv'

data = Data(filename)
# print(data)
data.show_data()

# in_x = []
# in_y = []
# count=int (input('point number'))
# for i in range(count):
#   in_x.append(float (input('x: ')))
#   in_y.append(float (input('y: ')))

# MAX_ERROR = 5/100

# plt.title('Good')

# for i in range(len(in_x)):
#   for j in range(len(data_x)):
#     if in_x[i] == data_x[j]:
#       limit = MAX_ERROR * data_y[j]
#       if data_y[j]-limit>in_y[i] or data_y[j] + limit < in_y[i]:
#         plt.title('Fault')

# plt.plot(data_x[0], data_y[0],color='black',marker='o')
# plt.plot(in_x, in_y, color='red',marker='d')
# plt.grid(color = 'gray')
# plt.xlabel('a')
# plt.ylabel('s')
# plt.show()

