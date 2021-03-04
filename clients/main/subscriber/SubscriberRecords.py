from os import path
from pathlib import Path
from matplotlib import pyplot as plt

class SubscriberRecords:
    data_lst = []
    filename = "DataPlot.png"
    filepath = None

    def __init__(self, host):
        # Assign file name
        self.filename = "Host#" + host.split(".")[-1] + self.filename

        # Init file path to save
        self._init_file_path()

    
    def _init_file_path(self):
        # Find the directory for saving
        currentdir = path.dirname(path.realpath(__file__))
        parentdir = path.dirname(path.dirname(path.dirname(currentdir)))

        # Create folder if doesn't exist
        self.filepath = path.join(parentdir, "assests")
        Path(self.filepath).mkdir(parents=True, exist_ok=True)

        # Append file name
        self.filepath = path.join(self.filepath, self.filename)


    def add(self, data: float):
        self.data_lst.append(data)
    
    
    def create_line_plot(self):
        x_var = [i for i in range(len(self.data_lst))]
        plt.plot(x_var, self.data_lst, '.-')
        plt.title(self.filename)
        plt.xlabel("Message #")
        plt.ylabel("Transmission Time (s)")
        plt.savefig(self.filepath, bbox_inches='tight')
        plt.show()