# CMPT 317.201809: Assignment 1 Question 1
# Given a target integer T, and a list of positive integers L
# Construct an expression using elements of L and
# integer operators + * // -
# so that the expression evaluates to T

# This implementation is pretty tricksy.  Several tricks are used to conserve memory and save time.
# 1.  The expression is not stored explicitly.  This reduces memory costs, as a string is more memory than an int.
#     The expression can be reconstructed by tracing the path from root to goal node.
# 2.  The choices available at any state are known only by examining path from initial state.  This saves
#     memory.  The cost of stepping through a state-chain is about the same as checking a list for numbers.
#     The memory savings is significant.  Instead of storing a list at every state, we store a single integer, and a
#     reference to the parent state.
# 3.  To avoid lots of string operations, we keep a small number of standard strings, and refer to them instead of
#     creating new stirngs all the time.  We use tuples to represent actions.  Lots of tuples are created and destroyed,
#     but almost no strings.  We don't have to convert back and forth from integers to strings, either.
#

import random as rand
import math as math

class State(object):
    """We store the value of the expression so far, primarily.
        To help ensure that choices are not reused, each state stores the current choice,
        and a reference to the state's parent.  This way we can ask: has a number been used?

    """
    def __init__(self, value, number, operation, parent_state):
        self.value = value
        self.choice = number
        self.prior_action = operation
        self.parent = parent_state

    def __str__(self):
        if self.value is None:
            return '< Initial state,' + str(self.choice) + '>'
        else:
            return '<'+ str(self.value) + ' by ' + self.prior_action + ' ' + str(self.choice) + '>'

    def used(self, c):
        """Examine the chain of states from self to the initial state, and
            check if value c appears as a choice.
            This check is probably a bit more expensive than 'c in list', but it
            keeps the amount of storage to a very small minimum."""

        if self.choice == c:
            return True
        elif self.parent is None:
            return False
        else:
            return self.parent.used(c)

    def expression(self):
        if self.value is None:
            return ""
        elif self.prior_action is Problem.action_start:
            return str(self.choice)
        elif self.prior_action is Problem.action_add:
            return '(' + self.parent.expression() + ') + ' + str(self.choice)
        elif self.prior_action is Problem.action_subtr:
            return '(' + self.parent.expression() + ') - ' + str(self.choice)
        elif self.prior_action is Problem.action_mult:
            return '(' + self.parent.expression() + ') * ' + str(self.choice)
        elif self.prior_action is Problem.action_div:
            return '(' + self.parent.expression() + ') // ' + str(self.choice)
        else:
            return "something really bad happened"

class InformedState(State):
    """We add an attribute to the state, namely a place to
        store the estimated path cost to the goal state.
    """
    def __init__(self, value, number, operation, parent_state, hval):
        super().__init__(value, number, operation, parent_state)
        self.hval = hval

class Problem(object):
    """The Problem class defines the transition model for states.
       To interact with search classes, the transition model is defined by:
            is_goal(s): returns true if the state is the goal state.
            actions(s): returns a list of all legal actions in state s
            result(s,a): returns a new state, the result of doing action a in state s
        Other methods here are not part of the interface.

        Constructor is given a target and a list of choices (integers).
    """

    # some constants for the class.  Referring to these will reduce string method costs!
    action_start = "load "
    action_add = "add "
    action_mult = "mult "
    action_subtr = "sub "
    action_div = "div "

    def __init__(self, target=None, choices=None):
        self.target = target
        self.choices = choices

    def create_initial_state(self):
        return State(None, None, None, None)


    def is_goal(self, a_state:State):
        """The target value is stored in the Problem instance."""
        return a_state.value == self.target

    def actions(self, a_state:State):
        """Returns all the actions that are legal in the given state.
            Here, an action is represented as a tuple (string, integer)
            The strings are the ones defined above as class attributes,
            so that we only ever have one copy of each of them.  Every
            action tuple refers to one of these strings.
        """
        actions = []
        if a_state.value is None:
            for c in self.choices:
                actions.append((self.action_start, c))
        else:
            for c in self.choices:
                if not a_state.used(c):
                    actions.append((self.action_add, c))
                    actions.append((self.action_mult, c))
                    actions.append((self.action_subtr, c))
                    actions.append((self.action_div, c))

        return actions

    def result(self, a_state:State, an_action):
        """Given a state and an action, return the resulting state.
           An action is a tuple (string, integer).
           To recognize an action, we compare string references using 'is'.
           Presumably, the string refers to one of the action strings defined above.
           This guarantees that the comparison is fast.
        """
        the_op = an_action[0]
        operand = an_action[1]
        if the_op is self.action_start:
            new_value = operand
        elif the_op is self.action_add:
            new_value = a_state.value + operand
        elif the_op is self.action_subtr:
            new_value = a_state.value - operand
        elif the_op is self.action_mult:
            new_value = a_state.value * operand
        elif the_op is self.action_div:
            new_value = a_state.value // operand
        else:
            # it's not one of the known strings.  Uh oh.
            new_value = None

        return State(new_value, operand, the_op, a_state)

    def random_instance(self, size, steps):
        """Creates a random instance of a problem.
           It just chooses random actions, and builds a random expression.
        """
        vals = rand.sample(range(1,10*size+1), size)
        state = State(None, None, None, None)
        for i in range(steps):
            actions = self.actions(state)
            act = rand.choice(actions)
            state = self.result(state,act)
        target = eval(state.value)
        return (target, vals, str(state.value))

class InformedProblem(Problem):
    """We add the ability to calculate an estiamte to the goal state.
    """
    def __init__(self, target=None, choices=None):
       super().__init__(target, choices)

    def create_initial_state(self):
        return InformedState(None, None, None, None, 0)

    def calc_h(self, target, value):
        """This function computes the heuristic function h(n)
           Here, we look at the difference between target and value.
           The bigger the difference, the more steps.
           However, to convert to steps, I use log10().

           The "relaxed problem" is one in which every action is "* 10".

           This heuristic is not admissible.  It can over-estimate.
           But it under-estimates a lot, too.

           Absolute value allows for negative differences, and adding 1
           means log10() won't die if value == target.  Rounding gets us to
           integer number of actions.
        """
        return int(round(math.log10(1+abs(target - value))))

    def result(self, a_state:State, an_action):
        """Given a state and an action, return the resulting state.
           An action is a tuple (string, integer).
           We add the heuristic value to the informed state here.
        """
        result = super().result(a_state, an_action)
        result.hval = self.calc_h(self.target, result.value)
        return result