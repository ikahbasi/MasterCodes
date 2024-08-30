import numpy as np

class XYZM:
    def __init__(self):
        self.LON   = []
        self.LAT   = []
        self.DEPTH = 0
        self.MAG   = 0
        self.PHUSD = 0
        self.NO_ST = 0
        self.MIND  = 0
        self.GAP   = 0
        self.RMS   = 0
        self.SEH   = 0
        self.SEZ   = 0
        self.YYYY  = 0
        self.MM    = 0
        self.DD    = 0
        self.HH    = 0
        self.MN    = 0
        self.SEC   = 0
    def read(self, file_name):
        data_file = np.genfromtxt(file_name, skip_header=1)
        self.LON   = data_file[:, 0]
        self.LAT   = data_file[:, 1]
        self.DEPTH = data_file[:, 2]
        self.MAG   = data_file[:, 3]
        self.PHUSD = data_file[:, 4]
        self.NO_ST = data_file[:, 5]
        self.MIND  = data_file[:, 6]
        self.GAP   = data_file[:, 7]
        self.RMS   = data_file[:, 8]
        self.SEH   = data_file[:, 9]
        self.SEZ   = data_file[:, 10]
        self.YYYY  = data_file[:, 11]
        self.MM    = data_file[:, 12]
        self.DD    = data_file[:, 13]
        self.HH    = data_file[:, 14]
        self.MN    = data_file[:, 15]
        self.SEC   = data_file[:, 16]
