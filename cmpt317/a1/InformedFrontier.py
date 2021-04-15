# CMPT 317.201809: A Python implementation of Frontier interfaces for informed search.
#
# Simple implementations of the Frontier interface.
#   Frontier: a base class
#   FrontierFIFO: implements FIFO, for use by BFS
#   FrontierLIFO: implements LIFO, for use by DFS
#

import heapq as heapq
from Frontier import Frontier


class FrontierPQ(Frontier):
    """This version is a priority queue.
       We use heappq here, because it's convenient.
       heappq uses a list as its underlying data structure.
       heapq uses normal tuple-ordering, which is fine,
       except when there is a tie.

       The data is stored as tuples (value, state),
       and the items are sorted according to value.
       However, when two values are equal, tuple ordering
       normally and reasonably looks at the rest of the tuple,
       and there's no good ordering for states.

       So we play a little trick here, and we simply keep track
       of how many items are added to the queue, putting a unique
       counted value in the tuple after the value:

       (value, number, state)

       No two entries will have the same number, eliminating ties.
       This has the added benefit of ensuring that when there are ties
       for value, the queue will produce the states in the order they
       were generated.
    """

    def __init__(self):
        Frontier.__init__(self)
        self._counter = 0

    def remove(self):
        """remove the state from the end"""
        val = heapq.heappop(self._nodes)
        # return the state only
        return val[2]


class FrontierUCS(FrontierPQ):
    """This version looks at path-cost for ordering"""

    def __init__(self):
        FrontierPQ.__init__(self)

    def add(self, aNode):
        """Add the new state on the end"""
        self._counter += 1
        heapq.heappush(self._nodes, (aNode.path_cost, self._counter, aNode))

class FrontierGBFS(FrontierPQ):
    """This version looks at hval for ordering"""

    def __init__(self):
        FrontierPQ.__init__(self)

    def add(self, aNode):
        """Add the new state on the end"""
        self._counter += 1
        heapq.heappush(self._nodes, (aNode.state.hval, self._counter, aNode))

class FrontierAStar(FrontierPQ):
    """This version looks at path-cost + hval for ordering"""

    def __init__(self):
        FrontierPQ.__init__(self)

    def add(self, aNode):
        """Add the new state on the end"""
        self._counter += 1
        # print(aNode.path_cost, aNode.state.hval)
        heapq.heappush(self._nodes, (aNode.path_cost + aNode.state.hval, self._counter, aNode))


