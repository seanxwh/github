import random
import copy
import math
import itertools


class GridWord(object):
    def __init__(self, states_value, states=None,  y_size=None, x_size=None, rewards = None, min_reward = None, max_reward = None, reward_step = None, actions_prob = None, trans_prob = None, next_states = None):
        self.x = x_size
        self.y = y_size
        self.minR = min_reward
        self.maxR = max_reward
        self.states = states if states else list(itertools.product(list(range(y_size)),list(range(x_size))))
        if states_value: self.states_value = copy.deepcopy(states_value)
        else:
            self.states_value = {}
            for state in self.states:
                self.states_value[state] = 0

        if rewards: self.rewards = rewards
        else:
            self.rewards = {}
            for state in self.states:
                self.rewards[state] = -1 if not min_reward or not max_reward or not reward_step else random.randrange(min_reward, max_reward,reward_step)
            self.rewards[(0,0)]= 0
            self.rewards[(y_size-1, x_size-1)]=0

        if actions_prob : self.actions_prob = actions_prob
        else:
            self.actions_prob={}
            for state in self.states:
                self.actions_prob[state] = [0.25]*4
            self.actions_prob[(0,0)] = [0,0,0,0]
            self.actions_prob[(y_size-1,x_size-1)]=[0,0,0,0]

        if trans_prob : self.trans_prob = trans_prob
        else:
            self.trans_prob = {}
            for state in self.states :
                for action_idx in range(len(self.actions_prob[state])):
                    self.trans_prob[(state, action_idx)] = [0,0,0,0]
                    if state == (0,0) or state == (y_size-1, x_size-1) : continue
                    else: self.trans_prob[(state, action_idx)][action_idx] = 1

        if next_states: self.next_states = next_states
        else:
            self.next_states = {}
            for state in self.states:
                y,x = state
                self.next_states[state] = self.Generate_Next_State(self.rewards, y, x)


    def Generate_Next_State(self, rewards, y, x):
        if rewards[(y,x)] == 0: return [(y,x),(y,x),(y,x),(y,x)]
        else:
            up_x_y = (y+1,x) if y+1<self.y else (y,x)
            dw_x_y = (y-1,x) if y-1>=0 else (y,x)
            lf_x_y = (y,x-1) if x-1>=0 else (y,x)
            rg_x_y = (y,x+1) if x+1<self.x else (y,x)
            return [lf_x_y, up_x_y, rg_x_y, dw_x_y]

    def Update_States(self, states_value):
        return GridWord(states_value, self.states, self.y, self.x , self.rewards, None, None, None, self.actions_prob, self.trans_prob, self.next_states)

    def Return_Rewards(self): return self.rewards

    def Return_States(self): return self.states

    def Return_States_Value(self): return self.states_value

    def Return_Transition_Prob(self) : return self.trans_prob

    def Return_Next_States(self): return self.next_states

    def Return_Actions_Prob(self): return self.actions_prob

    def Print_Reward(self):
        reward = [[None for i in range(self.x)] for k in range(self.y)]
        print "print rewards\n"
        for state in self.states:
            y,x = state
            reward[y][x] = self.rewards[state]
        self.Print(reward)

    def Print_World(self):
        world = [[None for i in range(self.x)] for k in range(self.y)]
        print "print world\n"
        for state in self.states:
            y,x = state
            world[y][x] = self.states_value[state]
        self.Print(world)

    def Print(self, matrix):
        print '['
        for row in matrix:
            print row
        print ']\n'


class ModelBasedReinforcementLearning(object):
    def __init__(self, simulation, delta, discount, method=None):
        self.simulation = simulation
        self.delta = delta
        self.discount = discount
        self.method = method

    def Start(self):
        if not self.method: return self.Start_Iterative_Policy_Evaluation()
        elif self.method == 1: return self.Start_Policy_Iteration()
        else: return self.Start_Value_Iteration()

    def Generate_Parameters(self):
            return self.Generate_Parameters_From_Two_Dim_Simulation() #higher function wrapper for generate parameters from the given simulation

    def Generate_Parameters_From_Two_Dim_Simulation(self):
        simulation = self.simulation
        new_states_value =  simulation.Return_States_Value()
        prev_states_value = copy.deepcopy(new_states_value)
        states = simulation.Return_States()
        actions_prob = simulation.Return_Actions_Prob()
        transition_prob = simulation.Return_Transition_Prob()
        discount = self.discount
        rewards = simulation.Return_Rewards()
        next_states = simulation.Return_Next_States()
        parameters = (new_states_value, prev_states_value, states, actions_prob, transition_prob, rewards, discount, next_states)
        return parameters

    def Update_Two_Dim_Simulation(self, states_value):
        simulation = self.simulation
        return simulation.Update_States(states_value)


    def Start_Iterative_Policy_Evaluation(self):
        parameters = self.Generate_Parameters_From_Two_Dim_Simulation()
        result = self.Policy_Evaluation(parameters)
        return self.Update_Two_Dim_Simulation(result)

    def Policy_Evaluation(self, parameters, flag = None):
        (new_states_value, prev_states_value, states, actions_prob, transition_prob, rewards, discount, next_states) = parameters
        while True:
            delta = 0
            for state in states:
                new_state_val = 0
                for action_idx in range(len(actions_prob[state])):
                    if actions_prob[state][action_idx] == 0: continue
                    state_action = (state, action_idx)
                    next_states_prob = transition_prob[state_action]
                    next_states_sum_given_state_action = 0
                    for next_state, next_state_prob in zip(next_states[state], next_states_prob):
                        next_states_sum_given_state_action += next_state_prob*(rewards[state]+discount*prev_states_value[next_state])
                    new_state_val +=  actions_prob[state][action_idx]*next_states_sum_given_state_action
                new_states_value[state] = new_state_val
                abs_dif = abs(new_states_value[state] - prev_states_value[state])
                delta = max(delta, abs_dif)
            if flag: return new_states_value
            if delta <= self.delta: return new_states_value
            prev_states_value = copy.deepcopy(new_states_value)


    def Start_Policy_Iteration(self):
        parameters = self.Generate_Parameters()
        (new_states_value, prev_states_value, states, actions_prob, transition_prob, rewards, discount, next_states) = parameters
        new_actions_prob = self.Generate_Random_Policy(states, actions_prob, rewards)
        new_parameters = (new_states_value, prev_states_value, states, new_actions_prob, transition_prob, rewards, discount, next_states)
        result = self.Policy_Iteration(new_parameters)
        return self.Update_Two_Dim_Simulation(result)

    def Generate_Random_Policy(self, states, actions_prob, reward):
        actions_prob_copy = copy.deepcopy(actions_prob)
        for state in states:
            idx = random.randrange(0,len(actions_prob[state])-1,1)
            actions_prob_copy[state] = [0 for i in range(len(actions_prob_copy[state]))]
            actions_prob_copy[state][idx] = 1 if reward[state] != 0 else 0
        return actions_prob_copy

    def Find_Greedy_Policy(self, parameters):
        (new_states_value, prev_states_value, states, actions_prob, transition_prob, rewards, discount, next_states) = parameters
        actions_prob_copy = copy.deepcopy(actions_prob)
        for state in states:
            new_states_val_by_action = []
            for action_idx in range(len(actions_prob_copy[state])):
                state_action = (state, action_idx)
                next_states_prob = transition_prob[state_action]
                next_states_sum_given_state_action = 0
                for next_state, next_state_prob in zip(next_states[state], next_states_prob):
                    next_states_sum_given_state_action += next_state_prob*(rewards[state]+discount*prev_states_value[next_state])
                new_states_val_by_action.append(next_states_sum_given_state_action)
            idx = new_states_val_by_action.index(max(new_states_val_by_action))
            actions_prob_copy[state] = [0 for i in range(len(actions_prob_copy[state]))]
            actions_prob_copy[state][idx] = 1
        return actions_prob_copy

    def Policy_Iteration(self,parameters):
        new_states_value = self.Policy_Evaluation(parameters, 1)
        (_, _, states, actions_prob, transition_prob, rewards, discount, next_states) = parameters
        new_parameters = (new_states_value, new_states_value, states, actions_prob, transition_prob, rewards, discount, next_states)
        greedy_policy = self.Find_Greedy_Policy(new_parameters)
        if actions_prob == greedy_policy:
            return new_states_value
        else:
            prev_states_value = copy.deepcopy(new_states_value)
            new_parameters = (new_states_value, prev_states_value, states, greedy_policy, transition_prob, rewards, discount, next_states)
            return self.Policy_Iteration(new_parameters)

    def Start_Value_Iteration(self):
        parameters = self.Generate_Parameters()
        result = self.Value_Iteration(parameters)
        return self.Update_Two_Dim_Simulation(result)

    def Value_Iteration(self,parameters):
        k =100
        (new_states_value, prev_states_value, states, actions_prob, transition_prob, rewards, discount, next_states) = parameters
        while True:
            delta = 0
            for state in states:
                new_state_val = -float('inf')
                for action_idx in range(len(actions_prob[state])):
                    state_action = (state, action_idx)
                    next_states_prob = transition_prob[state_action]
                    next_states_sum_given_state_action = 0
                    for next_state, next_state_prob in zip(next_states[state], next_states_prob):
                        next_states_sum_given_state_action += next_state_prob*(rewards[state]+discount*prev_states_value[next_state])
                    new_state_val = max(next_states_sum_given_state_action, new_state_val)
                new_states_value[state] = new_state_val
                abs_diff = abs(new_states_value[state]-prev_states_value[state])
                delta = max(delta, abs_diff)
            if delta <= self.delta: return new_states_value
            prev_states_value = copy.deepcopy(new_states_value)




print 'Policy Evaluation'
A1 = GridWord(None, None, 4, 4, None, None, None, None, None, None, None)
A1.Print_World()
A1.Print_Reward()


R1 = ModelBasedReinforcementLearning(A1, 0.001, 1, 0)
R1 = R1.Start()
R1.Print_World()
R1.Print_Reward()





print 'Policy Iteration'
A2 = GridWord(None, None, 4, 4, None, None, None, None, None, None, None)
A2.Print_World()
A2.Print_Reward()


R2 = ModelBasedReinforcementLearning(A2, None, 1, 1)
R2 = R2.Start()
R2.Print_World()
R2.Print_Reward()






print 'Value Iteration'
A3 = GridWord(None, None, 4, 4, None, None, None, None, None, None, None)
A3.Print_World()
A3.Print_Reward()


R3 = ModelBasedReinforcementLearning(A3, 0.01, 1, 2)
R3 = R3.Start()
R3.Print_World()
R3.Print_Reward()
