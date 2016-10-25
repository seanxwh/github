import random
import copy
import math


class GridWord(object):
    def __init__(self, world, x_size=None, y_size=None, rewards = None, minReward = None, maxReward = None, rewardStep=None, transProb = None, nextStates = None):
        self.x = x_size
        self.y = y_size
        self.minR = minReward
        self.maxR = maxReward
        if world:  self.world = copy.deepcopy(world)
        else:
            self.world = [[0 for k in range(x_size)] for i in range(y_size)]
            self.world[0][0]= 0
            self.world[-1][-1]=0

        if rewards: self.rewards = rewards
        else:
            self.rewards= self.generateRewards(x_size, y_size, minReward, maxReward, rewardStep)
            self.rewards[0][0]= 0
            self.rewards[-1][-1]=0

        if transProb : self.transProb = transProb
        else:
            self.transProb = [[[0.25]*4 for k in range(x_size)] for i in range(y_size)]
            self.transProb[0][0] = [0,0,0,0]
            self.transProb[-1][-1]=[0,0,0,0]

        if nextStates: self.nextStates = nextStates
        else: self.nextStates = self.generateNextStates()

    def generateNextStates(self):
        next_states = [[None for k in range(self.x)] for i in range(self.y)]
        for y_idx in range(self.y):
            for x_idx in range(self.x):
                next_states[y_idx][x_idx] = self.generateNextState(self.rewards, y_idx, x_idx)
        return next_states

    def generateNextState(self, rewards, y, x):
        if rewards[y][x] == 0: return [[y,x],[y,x],[y,x],[y,x]]
        else:
            up_x_y = [y+1,x] if y+1<self.y else [y,x]
            dw_x_y = [y-1,x] if y-1>=0 else [y,x]
            lf_x_y = [y,x-1] if x-1>=0 else [y,x]
            rg_x_y = [y,x+1] if x+1<self.x else [y,x]
            return [lf_x_y, up_x_y, rg_x_y, dw_x_y]

    def generateRewards(self, x_size, y_size, minVal, maxVal, rewardStep):
        if not minVal and not maxVal: return [[-1 for k in range(x_size)] for i in range(y_size)]
        return [[random.randrange(minVal, maxVal,rewardStep) for k in range(x_size)] for i in range(y_size)]

    def updateWorld(self, world):
        return GridWord(world, None, None, self.rewards, None, None, None, self.transProb, self.nextStates)

    def returnReward(self): return self.rewards

    def returnWorld(self): return self.world

    def returnTransitionProb(self) : return self.transProb

    def returnNextStates(self): return self.nextStates


    def printReward(self):
        print "print rewards\n"
        print "[\n",
        for i in self.rewards:
            print " ",i
        print "]","\n"

    def printWorld(self):
        print "print world\n"
        print "[\n"
        for i in self.world:
            print " ",i
        print "]","\n"



class ReinforcementLearning(object):
    def __init__(self, simulation, iteration, discount, method=None):
