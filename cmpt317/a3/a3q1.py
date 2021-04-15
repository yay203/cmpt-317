# Ye, Yang 11185374 yay203


class State(object):
    '''
    a state contain a matrix
    '''
    def __init__(self, mtx):
        self.mtx = mtx

    def display(self):
        for i in self.mtx:
            print(i)


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
        return State(self.matrix)

    def is_goal(self, a_state:State):
        '''
        check if a_state is goal state
        :param a_state: a state
        :return: True if it meet the goal
        '''
        a = []
        for i in a_state.mtx:
            a.extend(i)
        s = set(range(1, self.size + 1))
        for i in range(self.size):
            row = set(a[i * self.size + j] for j in range(self.size))
            col = set(a[j * self.size + i] for j in range(self.size))
            if row != s or col != s:
                return False
        return True

    def actions(self, a_state:State):
        '''

        :param a_state: a state
        :return: a list of all actions
        '''
        blank = []
        row = 0
        for r in a_state.mtx:
            col = 0
            for c in r:
                if c == 0:
                    for i in range(1, self.size+1):
                        blank.append((row, col, i))
                col += 1
            row += 1
        return blank

    def result(self, a_state:State, action):
        '''

        :param a_state: a state
        :param action: an action
        :return: a new state by accepting action
        '''
        row = action[0]
        col = action[1]
        num = action[2]
        new_matrix = []
        for r in a_state.mtx:
            new_row = []
            for c in r:
                new_row.append(c)
            new_matrix.append(new_row)
        new_matrix[row][col] = num
        return State(new_matrix)


