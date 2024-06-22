from . import doors, params
import numpy as np
import random
class Person:
    def __init__(self,Line):
        self.params = params.Params()
        self.Line = Line
        self.idPath = self.params.laneLength - 1#在self.Line上的相对位置
        self.Line.Path[-1] = self
        self.atdoor = 0#为0表示不在门前，为整数时表示需要n步出门
        self.type = "Person"
        self.Line.push(self)
        self.Changein = False
    def move(self, doorType, doorState,TotalLine):
        if self.idPath>=1:#不在门前，前面无物体时前进一格
            if self.Line.Path[self.idPath-1]==None:
                self.Line.Path[self.idPath-1] = self
                self.Line.Path[self.idPath] = None
                self.idPath-=1
                if self.idPath == 0:
                    ifsucceccss = np.random.random()
                    self.params.generate_tg()
                    if ifsucceccss <= self.params.successRate: # successfully opened the door
                        # generate service time according to negative exp
                        self.atdoor = (
                            self.params.tg + 
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
                self.ChangeLine(TotalLine)
        else:
            self.atdoor -= self.params.timestep
            if self.atdoor == 0:#离开车道流程
                self.Line.Path[self.idPath] = None
                self.Line.utipass()
    def ChangeLine(self,TotalLine:list):
        """
            行人的换道函数，当且仅当：
            2.其所在位置前一格处有实体存在使其无法执行move()；
            3.其左右的Line上，至少有一条Line满足:这条Line上与行人平齐的一格及其前面一格均不存在实体；
            时，以self.params.ps为概率执行一次换道，移至新道路上与原位置平齐位置的前面一格。
            oxo ChangeLine() pxo    oxp
            opo -----------> ooo or ooo
        """
        if TotalLine==None:
            return
        if self.idPath==0:         
            return
        if self.Line.Path[self.idPath-1] == None:
            return
        if random.random()<self.params.ps:
            return
        ValidNeighbourLine = []
        for i in [-1,1]:
            if self.Line.idLine+i>=0 and self.Line.idLine+i<len(TotalLine):
                CandidateLine = TotalLine[self.Line.idLine+i]
                if CandidateLine.Path[self.idPath]==None and CandidateLine.Path[self.idPath-1]==None:
                    ValidNeighbourLine.append(CandidateLine)
        if len(ValidNeighbourLine)>0:
            DesLine =random.sample(ValidNeighbourLine,1)
            DesLine = DesLine[0]
            self.Line.Path[self.idPath] = None
            DesLine.Path[self.idPath-1] =self
            self.Line.updateAllutility()
            DesLine.updateAllutility()
            self.idPath-=1
            self.Line = DesLine
            self.Changein = True