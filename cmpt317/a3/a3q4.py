# Ye, Yang 11185374 yay203


class Variable(object):
    '''
    variable consists its domain, value, and a boolean consistent(True as default)
    '''
    def __init__(self,  domain, val=None, consistent=True):
        self.val = val
        self.domain = set(range(1, domain+1))
        self.consistent= consistent

    def display(self):
        return self.val


class State(object):
    '''
    a state consists of matrix sie, blank location record in a set
    '''
    def __init__(self, size, blank_location=None, ):
        self.size = size
        collection = {}
        for row in range(0,size):
            for col in range(0,size):
                collection['('+str(row)+', '+str(col)+')'] = Variable(size)
        self.collection = collection
        self.blank_location = blank_location

    def display(self):
        print('size:', self.size)
        for i in self.collection.keys():
            print(i, 'value:', self.collection[i].val, 'domain:', self.collection[i].domain)
        print(self.blank_location)


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
        initialize the state, accept data in to de collection, and restricts the domain of blank variable
        :return: an initial state
        '''
        initial_state = State(self.size)
        initial_state.blank_location = set()
        for row in range(0,self.size):
            for col in range(0,self.size):
                    initial_state.collection['('+str(row)+', '+str(col)+')'].val = self.matrix[row][col]
        for r in range(0,self.size):
            for c in range(0,self.size):
                if initial_state.collection['('+str(r)+', '+str(c)+')'].val == 0:
                    initial_state.blank_location.add((r,c))
        for i in initial_state.blank_location:
            for l in range(0, self.size):
                initial_state.collection[str(i)].domain.discard(self.matrix[i[0]][l])
                initial_state.collection[str(i)].domain.discard(self.matrix[l][i[1]])
                if initial_state.collection[str(i)].domain == set():
                    initial_state.collection[str(i)].consistent = False
        return initial_state

    def is_goal(self, a_state:State):
        '''
        check if the state meet the goal state
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
        :return: all the possible actions(in its domain) in a list
        '''
        blank = []
        for r in range(a_state.size):
            for c in range(a_state.size):
                if a_state.collection['('+str(r)+', '+str(c)+')'].val == 0:
                    if a_state.collection['('+str(r)+', '+str(c)+')'].consistent == False:
                        return []
                    for i in a_state.collection['('+str(r)+', '+str(c)+')'].domain:
                        blank.append((r, c, i))
        return blank

    def result(self, a_state:State, action):
        '''

        :param a_state: a state
        :param action: an anction
        :return: a new state by accepting an action
        '''
        r = action[0]
        c = action[1]
        num = action[2]
        new_state = State(a_state.size)
        for row in range(0,self.size):
            for col in range(0,self.size):
                new_state.collection['('+str(row)+', '+str(col)+')'].val = a_state.collection['('+str(row)+', '+str(col)+')'].val
        a_state.blank_location.discard((r, c))
        new_state.blank_location = set()
        for i in a_state.blank_location:
            new_state.blank_location.add(i)
        new_state.collection['('+str(r)+', '+str(c)+')'].val = num
        #for i in new_state.blank_location:
            #new_state.collection[str(i)].domain.discard(num)
        for i in new_state.blank_location:
            for l in range(0, self.size):
                new_state.collection[str(i)].domain.discard(self.matrix[i[0]][l])
                new_state.collection[str(i)].domain.discard(self.matrix[l][i[1]])
        return new_state