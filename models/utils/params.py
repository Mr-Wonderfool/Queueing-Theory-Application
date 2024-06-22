import numpy as np
"""Parameters used in simulation process"""
class Params:
    def __init__(self):
        self.timestep = .5#每个离散步长度
        self.tpenal = 2 * self.timestep
        self.to, self.tc = self.timestep, self.timestep
        self.tg = self.timestep
        self.tp = 0. # combine swap time and pass time into negative exponential

        self.laneNum = 1
        self.successRate = .4
        self.laneLength = 40
        self.ps = .5 # prob for switching lane
        self.isPerson = 1.
        self.isGenerate = .2 # TODO: change to poisson process
    def generate_tg(self):
        mu = 1. / (2*self.timestep)
        tmp = np.round(np.random.exponential(1. / mu) / self.timestep)
        tmp = max(min(tmp, 6), 1)
        self.tg = tmp * self.timestep
