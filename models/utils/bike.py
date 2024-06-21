from . import doors, params
import numpy as np
class Bicycle:
    def __init__(self,Line):
        self.params = params.Params()
        self.Line= Line
        self.headidPath = self.params.laneLength-2#车头在self.Line上的位置
        self.tailidPath = self.params.laneLength-1#车尾在self.Line上的位置
        self.Line.Path[-2] = self
        self.Line.Path[-1] = self#车头与车尾均在self.Line上作标记
        self.atdoor = 0#与上同：>1时车头在门前，=1时车尾在门前（车头已出门）
        self.type = "Bicycle"
        self.Line.push(self)
    def move(self, doorType, doorState):
        if self.headidPath>=1:#与上同
            if self.Line.Path[self.headidPath-1]==None:
                self.Line.Path[self.headidPath-1] = self
                self.Line.Path[self.tailidPath] = None
                self.headidPath -= 1
                self.tailidPath -= 1
                if self.headidPath == 0:
                    ifsucceccss = np.random.random()
                    if ifsucceccss <= self.params.successRate: # successfully opened the door
                        self.atdoor = (
                            self.params.tp + self.params.tg + 
                            doorType.value * self.params.tc + doorState.value * self.params.to
                        )
                        if doorType == doors.DoorType.keepOpen:
                            doorState = doors.DoorState.open
                    else:
                        self.atdoor = (
                            self.params.tg + self.params.tpenal + 
                            (1 - doorType.value) * (1 - doorState.value) * self.params.tc
                        )
                        doorState = doors.DoorState.close
        else:
            self.atdoor -= self.params.timestep        
            if self.atdoor == 1:#=1时前进一格，车尾留在门前
                self.Line.Path[self.tailidPath] = None
                self.headidPath = -1
                self.tailidPath = 0
            if self.atdoor==0:#完全离开
                self.Line.Path[self.tailidPath] = None
                self.Line.utipass()