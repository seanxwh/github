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
        self.simulation = simulation
        self.iteration = iteration
        self.discount = discount
        self.method = method


    def start(self):
        if not self.iteration: return self.simulation
        else:
            if not self.method: return self.PolicyEvaluation(self.simulation, self.iteration, self.discount)
            elif self.method == 1: return self.StartPolicyIteration(self.simulation, self.iteration, self.discount)
            else: return self.ValueIteration(self.simulation, self.iteration, self.discount)

    def MatrixRoundingDigit(self, matrix, digit):
        y,x = len(matrix),len(matrix[0])
        for y_idx in range(y):
            for x_idx in range(x):
                matrix[y_idx][x_idx] = round(matrix[y_idx][x_idx],digit)
        return matrix

    def GenerateParametersFromSimulation(self, simulation):
        currentWorldValue =  simulation.returnWorld()
        transitionProb = simulation. returnTransitionProb()
        rewards = simulation.returnReward()
        nextStates = simulation.returnNextStates()
        y,x = len(currentWorldValue),len(currentWorldValue[0])
        dummy = copy.deepcopy(currentWorldValue)
        return (currentWorldValue, transitionProb, rewards, nextStates, y, x, dummy)

    def PolicyEvaluation(self, simulation, iteration, discount):
        if not iteration or iteration==0: return simulation
        (currentWorldValue, transitionProb, rewards, nextStates, y, x, dummy) = self.GenerateParametersFromSimulation(simulation)
        for y_idx in range(y):
            for x_idx in range(x):
                tmpSum = 0
                for [nx_y, nx_x], prob in zip(nextStates[y_idx][x_idx],transitionProb[y_idx][x_idx]):
                    tmpSum += prob*(discount*dummy[nx_y][nx_x])
                currentWorldValue[y_idx][x_idx] = rewards[y_idx][x_idx]+tmpSum
        if iteration == 1: currentWorldValue = self.MatrixRoundingDigit(currentWorldValue,3)
        new_simulation = simulation.updateWorld(currentWorldValue)
        return self.PolicyEvaluation(new_simulation, iteration-1, discount)

    def ValueIteration(self, simulation, iteration, discount):
        if not iteration or iteration==0: return simulation
        (currentWorldValue, transitionProb, rewards, nextStates, y, x, dummy) = self.GenerateParametersFromSimulation(simulation)
        for y_idx in range(y):
            for x_idx in range(x):
                tmp = -float('inf')
                choosen_action_value = 0
                for [nx_y, nx_x], prob in zip(nextStates[y_idx][x_idx],transitionProb[y_idx][x_idx]):
                    tmp = max(rewards[y_idx][x_idx]+prob*discount*dummy[nx_y][nx_x], tmp)
                    if tmp == rewards[y_idx][x_idx]+prob*discount*dummy[nx_y][nx_x]:
                        choosen_action_value = tmp
                currentWorldValue[y_idx][x_idx] = tmp

        if iteration == 1: currentWorldValue = self.MatrixRoundingDigit(currentWorldValue,3)
        new_simulation = simulation.updateWorld(currentWorldValue)
        return self.ValueIteration(new_simulation, iteration-1, discount)

    def StartPolicyIteration(self, simulation, iteration, discount):
        if not iteration or iteration==0: return simulation
        currentWorldValue =  simulation.returnWorld()
        nextStates = simulation.returnNextStates()
        y,x = len(currentWorldValue),len(currentWorldValue[0])
        RandomPolicyMatrix = [[random.randrange(0,len(nextStates[i][k])-1,1) for k in range(x)] for i in range(y)]
        return self.PolicyIteration(RandomPolicyMatrix,simulation, iteration, discount)

    def PolicyIteration(self, policyMatrix, simulation, iteration, discount):
        if not iteration or iteration==0: return simulation
        (currentWorldValue, transitionProb, rewards, nextStates, y, x, dummy) = self.GenerateParametersFromSimulation(simulation)
        for y_idx in range(y):
            for x_idx in range(x):
                chooseAction = policyMatrix[y_idx][x_idx]
                nx_y, nx_x = nextStates[y_idx][x_idx][chooseAction]
                currentWorldValue[y_idx][x_idx] = rewards[y_idx][x_idx]+discount*dummy[nx_y][nx_x]
        new_simulation = simulation.updateWorld(currentWorldValue)

        nxPolicyMatrix = copy.deepcopy(policyMatrix)
        for y_idx in range(y):
            for x_idx in range(x):
                choosen_action_value = None
                counter = 0
                tmp = None
                for [nx_y, nx_x], prob in zip(nextStates[y_idx][x_idx],transitionProb[y_idx][x_idx]):
                    newStateValue = discount*new_simulation.returnWorld()[nx_y][nx_x]
                    tmp = max(rewards[y_idx][x_idx]+prob*newStateValue, tmp)
                    if tmp == rewards[y_idx][x_idx]+prob*newStateValue:
                        choosen_action_value = counter
                    counter += 1
                nxPolicyMatrix[y_idx][x_idx] = choosen_action_value
        return self.PolicyIteration(nxPolicyMatrix, new_simulation, iteration-1, discount)



A = GridWord(None, 4, 4, None, None, None, None, None, None)
A.printWorld()
#A.printReward()


R =  ReinforcementLearning(A, 900, 1)
R = R.start()
R.printWorld()
#R.printReward()

C = ReinforcementLearning(R, 900, 1)
C = C.start()
C.printWorld()
#C.printReward()



D = GridWord(None, 4, 4, None, None, None, None, None, None)
D.printWorld()
D.printReward()

R2 = ReinforcementLearning(D, 900, 1, 2)
R2 = R2.start()
R2.printWorld()



E = GridWord(None, 4, 4, None, None, None, None, None, None)
E.printWorld()

R3 = ReinforcementLearning(E, 900, 1, 1)
R3 = R3.start()
R3.printWorld()
