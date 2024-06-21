"""Parameters used in simulation process"""
class Params:
    def __init__(self):
        self.timestep = .5#每个离散步长度
        self.tpenal = 2 * self.timestep
        self.to, self.tc = self.timestep, self.timestep
        self.tg = self.timestep
        self.tp = self.timestep # TODO: change to poisson process for stochastic model

        self.laneNum = 1
        self.successRate = .9
        self.laneLength = 30
        self.ps = .5 # prob for switching lane
        self.isPerson = 1.
        self.isGenerate = .5 # TODO: change to poisson process