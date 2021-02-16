import os
from matplotlib import pyplot as plt

class DataPlot:
    dataSet = []
    filename = "DataPlot.png"

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
        plt.savefig(self.filename, dpi=300, bbox_inches='tight', pad=0.1)
        plt.show()