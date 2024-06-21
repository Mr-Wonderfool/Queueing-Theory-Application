from . import doors, params
import numpy as np
class Person:
    def __init__(self,Line):
        self.params = params.Params()
        self.Line = Line
        self.idPath = self.params.laneLength - 1#在self.Line上的相对位置
        self.Line.Path[-1] = self
        self.atdoor = 0#为0表示不在门前，为整数时表示需要n步出门
        self.type = "Person"
        self.Line.push(self)
    def move(self, doorType, doorState):
        if self.idPath>=1:#不在门前，前面无物体时前进一格
            if self.Line.Path[self.idPath-1]==None:
                self.Line.Path[self.idPath-1] = self
                self.Line.Path[self.idPath] = None
                self.idPath-=1
                if self.idPath == 0:
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
            if self.atdoor == 0:#离开车道流程
                self.Line.Path[self.idPath] = None
                self.Line.utipass()