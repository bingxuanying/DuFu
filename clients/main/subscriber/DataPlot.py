import os
from matplotlib import pyplot as plt

class DataPlot:
    dataSet = []
    filename = " Data Plot.png"

    def __init__(self, host):
        self.filename = "Host#" + host.split(".")[-1] + self.filename

    def add(self, data: float):
        self.dataSet.append(data)
    
    def createLinePlot(self):
        x_var = [i for i in range(len(self.dataSet))]
        plt.plot(x_var, self.dataSet, '.-')
        plt.title(self.filename)
        plt.xlabel("Message #")
        plt.ylabel("Transmission Time (s)")
        
        my_path = os.path.realpath(__file__) # Figures out the absolute path for you in case your working directory moves around.
        my_file = 'graph.png'
        plt.show()
        plt.savefig(os.path.join(my_path, "../", my_file))