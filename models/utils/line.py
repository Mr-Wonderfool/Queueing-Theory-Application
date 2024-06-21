import sys
from . import doors, params, person, bike
import numpy as np
import time
class Line:
    #车道类
    def __init__(self, doorType):
        self.params = params.Params()
        self.Path = [None]*self.params.laneLength#路段（Path）各节处的状况，为空时对应元素None,否则存储一个Person类或Bicycle类
        self.PassingCounter = 0#通过实体计数器
        self.Allutility = []#当前车道上的所有实体
        self.doorType = doorType
    def update(self):
        #对当前车道上的所有实体进行一次移动，先进队者先动
        doorState = doors.DoorState.open
        if self.doorType == doors.DoorType.normal:
            doorState = doors.DoorState.close
        elif self.doorType == doors.DoorType.keepOpen:
            doorState = doors.DoorState.open
        for i in self.Allutility:
            i.move(self.doorType, doorState)
    def generate(self):
        #满足条件时在最后随机生成人或单车
        if self.Path[-1]==None:#队尾为空
            ifgenerate = np.random.random()#是否生成实体的随机数
            if ifgenerate <= self.params.isGenerate:
                if self.Path[-2]==None:
                    ifperson = np.random.random()#是否生成人的随机数
                    if ifperson <= self.params.isPerson:
                        person.Person(self)
                    else:
                        bike.Bicycle(self)              
                else:
                    person.Person(self)
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
                str = str+"😡"
            elif "Bicycle" == self.Path[i].type:
                str = str+"🚲"+" "
                i += 1
            i += 1
        print(str,end=" ")
        time.sleep(self.params.timestep)#连续输出时每次间隔一个时间步
        sys.stdout.flush()
    def forward(self, print=False):
        #Line完整的执行一次时间步模拟的封装函数
        self.update()
        self.generate()
        if print:
            self.print()