# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        weightConstant = 1 # use to weight whether the pac's future move is too close to ghost
        ghostsDst = [util.manhattanDistance(newPos, ghostPos) for ghostPos in successorGameState.getGhostPositions() ]
        if (1 in ghostsDst):
            weightConstant = 0 # if the pac's future move made pac and ghost only one step away
        score = betterEvaluationFunction(successorGameState)
        return weightConstant*score


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)



class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        return self.maxLayer(gameState, 0) # the root is a maxLayer since alpha-beta also use root to control node expandsion

    def maxLayer(self, gameState, currentDepth):
        if (currentDepth == self.depth or gameState.isLose() or gameState.isWin()):
            return self.evaluationFunction(gameState)
        v = float('-inf')
        if currentDepth==0: record = []
        legalActions = gameState.getLegalActions()
        for action in legalActions:
            pacmanState = gameState.generateSuccessor(0,action)
            score = self.minLayer(pacmanState, currentDepth, 1)
            if currentDepth==0: record.append(score) # append the max score for each move at root(depth 0)
            v = max(v,score)
        if currentDepth==0:
            index = record.index(v)
            return legalActions[index]
        elif currentDepth!=0:
            return v

    def minLayer(self, gameState, currentDepth, agentIndex = 1): #the min action start from the 1st agent when call by maxLayer
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        v = float('inf')
        ghostActions = gameState.getLegalActions(agentIndex)
        for ghostAction in ghostActions:
            ghostsState = gameState.generateSuccessor(agentIndex,ghostAction)
            if agentIndex < gameState.getNumAgents()-1: # repeat minLayer with the next agent(for multiple opponents)
                score = self.minLayer(ghostsState, currentDepth, agentIndex+1)
            elif agentIndex == gameState.getNumAgents()-1: #call the maxLayer when is last opponent's turn, to expand the maxLayer
                score = self.maxLayer(ghostsState, currentDepth+1)
            v = min(v, score)
        return v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # initialize alpha and beta
        alpha = float('-inf')
        beta = float('inf')
        return self.maxLayer(gameState, 0 , alpha, beta) # the root is a maxLayer since alpha-beta also use root to control node expandsion
# method 1
    def maxLayer(self, gameState, currentDepth, alpha, beta):
        if (currentDepth == self.depth or gameState.isLose() or gameState.isWin()):
            return self.evaluationFunction(gameState)
        v = float('-inf')
        if currentDepth==0: record = []
        legalActions = gameState.getLegalActions()
        for action in legalActions:
            pacmanState = gameState.generateSuccessor(0,action)
            score = self.minLayer(pacmanState, currentDepth, alpha, beta, 1)
            if currentDepth==0: record.append(score) # append the max score for each move at root(depth 0)
            v = max(v,score)
            if v>beta: return v # return if v is greater than alpha from the upper layer(min), because min layer will not pick this node
            alpha = max(alpha,v)
        if currentDepth==0:
            index = record.index(v)
            return legalActions[index]
        elif currentDepth!=0:
            return v

    def minLayer(self, gameState, currentDepth, alpha, beta, agentIndex = 1): #the min action start from the 1st agent when call by maxLayer
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        v = float('inf')
        ghostActions = gameState.getLegalActions(agentIndex)
        for ghostAction in ghostActions:
            ghostsState = gameState.generateSuccessor(agentIndex,ghostAction)
            if agentIndex < gameState.getNumAgents()-1: # repeat minLayer with the next agent(for multiple opponents)
                score = self.minLayer(ghostsState, currentDepth, alpha, beta, agentIndex+1)
            elif agentIndex == gameState.getNumAgents()-1: #call the maxLayer when is last opponent's turn, to expand the maxLayer
                score = self.maxLayer(ghostsState, currentDepth+1, alpha, beta)
            v = min(v, score)
            if v<alpha:return v # return if v is less than alpha from the upper layer(max), because max layer will not pick this node
            beta = min(beta,v)
        return v

# method 2
    # def maxLayer(self, gameState, currentDepth, alpha, beta):
    #
    # def minLayer(self, gameState, currentDepth, alpha, beta, agentIndex = 1):
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        return self.maxLayer(gameState, 0) # the root is a maxLayer since alpha-beta also use root to control node expandsion

    def maxLayer(self, gameState, currentDepth):
        if (currentDepth == self.depth or gameState.isLose() or gameState.isWin()):
            return self.evaluationFunction(gameState)
        v = float('-inf')
        if currentDepth==0: record = []
        legalActions = gameState.getLegalActions()
        for action in legalActions:
            pacmanState = gameState.generateSuccessor(0,action)
            score = self.expLayer(pacmanState, currentDepth, 1)
            if currentDepth==0: record.append(score) # append the max score for each move at root(depth 0)
            v = max(v,score)
        if currentDepth==0:
            index = record.index(v)
            return legalActions[index]
        elif currentDepth!=0:
            return v

    def expLayer(self, gameState, currentDepth, agentIndex = 1):
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        v =[]
        ghostActions = gameState.getLegalActions(agentIndex)
        for ghostAction in ghostActions:
            ghostsState = gameState.generateSuccessor(agentIndex,ghostAction)
            if agentIndex < gameState.getNumAgents()-1:
                score = self.expLayer(ghostsState, currentDepth, agentIndex+1)
            elif agentIndex == gameState.getNumAgents()-1:
                score = self.maxLayer(ghostsState, currentDepth+1)
            v.append(score)
        avg = float(sum(v)/len(v))
        return avg


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    def heuristicFunction(successorGameState):
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        FoodsDst = []
        rowNum = 0
        for foodDst in newFood: # return the coordinates of the food in row and col
            colNum = 0
            for itm in foodDst:
                if itm == True:
                    FoodsDst.append((rowNum,colNum))
                colNum+=1
            rowNum+=1
        if FoodsDst:
            foodsDst =[util.manhattanDistance(newPos, foodPos) for foodPos in FoodsDst]
            minFoodsDst = min(foodsDst)
            maxFoodsDst = max(foodsDst)
            avgFoodsDst = sum(foodsDst)/len(foodsDst)
            return (successorGameState.getScore()
                -(maxFoodsDst+minFoodsDst+avgFoodsDst)
                +sum(random.sample((maxFoodsDst,minFoodsDst,avgFoodsDst),2))
                +sum(newScaredTimes))
        elif len(FoodsDst)==0: # if the move eat the last food in the game
            return successorGameState.getScore()
    return heuristicFunction(currentGameState)
# Abbreviation
better = betterEvaluationFunction
