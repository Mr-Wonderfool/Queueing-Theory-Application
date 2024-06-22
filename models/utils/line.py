import sys
from . import doors, params, person, bike
import numpy as np
import time
import random
class Line:
    #车道类
    def __init__(self, doorType,idLine = 0):
        self.params = params.Params()
        self.Path = [None]*self.params.laneLength#路段（Path）各节处的状况，为空时对应元素None,否则存储一个Person类或Bicycle类
        self.PassingCounter = 0#通过实体计数器
        self.Allutility = []#当前车道上的所有实体
        self.doorType = doorType
        self.idLine = idLine#车道在总车道列表中的id，id相邻者视为道路相邻。
    def update(self,TotalLine):
        #对当前车道上的所有实体进行一次移动，先进队者先动
        doorState = doors.DoorState.open
        if self.doorType == doors.DoorType.normal:
            doorState = doors.DoorState.close
        elif self.doorType == doors.DoorType.keepOpen:
            doorState = doors.DoorState.open
        for i in self.Allutility:
            i.move(self.doorType, doorState,TotalLine)
    def PoissionStream(self,TotalLine:list=None):
        if TotalLine == None:#单Line情形
            if self.Path[-1]==None and self.params.unlinedPersonNum>0:#队尾为空且有人预备进队
                person.Person(self)#队尾生成人
                self.params.unlinedPersonNum-=1#预备进队人数减一
            self.params.unlinedPersonNum += np.random.poisson(self.params.crowdType)
        else:
            if TotalLine.index(self)==0:#整个车道队全盘模拟一时间步时第一次调用该函数，分配人群
                AvailableLine = []
                for line in TotalLine:
                    if line.Path[-1]==None:
                        AvailableLine.append(line)#筛选有空格的Line
                if len(AvailableLine)<=self.params.unlinedPersonNum:#空位少于预备进队人数，所有空位生成一人
                    for line in AvailableLine:
                        person.Person(line)
                    self.params.unlinedPersonNum-=len(AvailableLine)
                else:#空位多于预备进队人数，随机挑选空位全部分配
                    ChoosenLine = random.sample(AvailableLine,self.params.unlinedPersonNum)
                    for line in ChoosenLine:
                        person.Person(line)
                    self.params.unlinedPersonNum=0
            if TotalLine.index(self) == len(TotalLine)-1:#整个车道队全盘模拟一时间步时最后一次一次调用该函数，生成人群
                self.params.unlinedPersonNum += np.random.poisson(self.params.crowdType)
    def utipass(self):
            #为每个实体的move()调用，打包有实体通过门时对应Line的行为
            self.PassingCounter+=1#计数器+1
            self.Allutility.pop(0)#将通过的实体弹出队列
            #path置空位于每个实体的move函数中
    def push(self,Util):
            #向Line加入某个实体的打包
        self.Allutility.append(Util)
    def print(self):
        #打印Line各段path上的信息，简单的可视化
        str = "\r"
        i = 0
        while i < len(self.Path):
            if None == self.Path[i]:
                str = str+"🈳"
            elif "Person" == self.Path[i].type:
                if self.Path[i].Changein == False:
                    str = str+"😡"
                else:
                    str = str+"😀"
            elif "Bicycle" == self.Path[i].type:
                str = str+"🚲"+" "
                i += 1
            i += 1
        print(str,end = " ")
        time.sleep(0.1*self.params.timestep)#连续输出时每次间隔一个时间步
        sys.stdout.flush()
    def forward(self,TotalLine = None,print=False):
        #Line完整的执行一次时间步模拟的封装函数
        self.update(TotalLine)
        if print:
            self.print()
        self.PoissionStream(TotalLine)
    def count_occupied(self):
        """Count the block occupied in a certain time"""
        return sum(x is not None for x in self.Path)
    def updateAllutility(self):
        """
            在有人换道进入时，根据self.Path记录的信息更新self.Allutility
        """
        self.Allutility = []
        PreventRepeat = []
        for x in self.Path:
            if x != None:
                if x not in PreventRepeat:
                    PreventRepeat.append(x)
                    self.Allutility.append(x)