# Ye, Yang 11185374 yay203


class Variable(object):
    '''
    variable consist its value and its domain
    '''
    def __init__(self,  domain, val=None):
        self.val = val
        self.domain = list(range(1,domain+1))

    def display(self):
        return self.val


class State(object):
    '''
    state include the matrix size and a matrix consist of variables
    '''
    def __init__(self, size):
        self.size = size
        collection = {}
        for row in range(0,size):
            for col in range(0,size):
                collection['('+str(row)+','+str(col)+')'] = Variable(size)
        self.collection = collection

    def display(self):
        print('size:', self.size)
        for i in self.collection.keys():
            print(i, 'value:', self.collection[i].val, 'domain:', self.collection[i].domain)


class Problem(object):
    """The Problem class defines the transition model for states.
       To interact with search classes, the transition model is defined by:
            is_goal(a_state): returns true if the state is the goal state.
            actions(a_state: return all the action of the matrix
            result(a_state,action): a_state accept an action and return a new state by do an action
        Constructor is a matrix about the latin square(incomplete), and its size
    """
    def __init__(self, matrix, size):
        self.matrix = matrix
        self.size = size

    def initial_state(self):
        '''
        accept all the matrix value and store in the state's variable, if it is '_', store 0
        :return:
        '''
        initial_state = State(self.size)
        for row in range(0,self.size):
            for col in range(0,self.size):
                    initial_state.collection['('+str(row)+','+str(col)+')'].val = self.matrix[row][col]
        return initial_state

    def is_goal(self, a_state:State):
        '''
        check if a_state is the goal state
        :param a_state: a state
        :return: True if it is goal state, else return False
        '''
        goal = set(range(1,a_state.size+1))
        c = []
        for i in a_state.collection.values():
            if i.val == 0:
                return False
            c.append(i.val)
        for i in range(self.size):
            row = set(c[i * self.size + j] for j in range(self.size))
            col = set(c[j * self.size + i] for j in range(self.size))
            if row != goal or col != goal:
                return False
        return True

    def actions(self, a_state:State):
        '''

        :param a_state: a state
        :return: return all actions in a list
        '''
        blank = []
        for r in range(a_state.size):
            for c in range(a_state.size):
                if a_state.collection['('+str(r)+','+str(c)+')'].val == 0:
                    for i in range(1, a_state.size+1):
                        blank.append((r, c, i))
        return blank

    def result(self, a_state:State, action):
        '''

        :param a_state: a state
        :param action: an action
        :return: a new state by accepting the action
        '''
        r = action[0]
        c = action[1]
        num = action[2]
        new_state = State(a_state.size)
        for row in range(0,self.size):
            for col in range(0,self.size):
                    new_state.collection['('+str(row)+','+str(col)+')'].val = a_state.collection['('+str(row)+','+str(col)+')'].val
        new_state.collection['('+str(r)+','+str(c)+')'].val = num
        return new_state




