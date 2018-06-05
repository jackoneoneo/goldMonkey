import plotly.plotly as py
from plotly.graph_objs import *
import  os
'''
trace0 = Scatter(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17]
)
trace1 = Scatter(
    x=[1, 2, 3, 4],
    y=[16, 5, 11, 9]
)
data = Data([trace0, trace1])

py.offline.plot(data, filename = 'basic-line')
'''

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    else:
        pass
pathDir = "E:\\上都电厂数据\\"

for i in range(9):
    for j in range(4):
        mkdir(pathDir+str(i+1)+"-"+str(j+1))
