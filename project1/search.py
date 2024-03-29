# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    """
    
    Start: (5, 5)
    Is the start a goal? False
    Start's successors: [((5, 4), 'South', 1), ((4, 5), 'West', 1)]

    """

    # dfs uses a stack to keep track of frontier
    stack = util.Stack()
    parents = {}
    actions = []
    visited = set()

    root = (problem.getStartState(), None, None)
    stack.push(root)

    while (not stack.isEmpty()):
        current = stack.pop()
        visited.add(current[0])

        if problem.isGoalState(current[0]):
            while current != root:
                actions.append(current[1])
                current = parents[current]
            actions.reverse()

            return actions

        for successor in problem.getSuccessors(current[0]):
            if successor[0] not in visited:
                stack.push(successor)
                parents[successor] = current

    return None


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    # bfs uses a queue to keep track of frontier
    queue = util.Queue()
    parents = {}
    actions = []
    visited = set()

    root = (problem.getStartState(), None, None)
    queue.push(root)
    visited.add(root[0])

    while (not queue.isEmpty()):
        current = queue.pop()
        if problem.isGoalState(current[0]):
            while current != root:
                actions.append(current[1])
                current = parents[current]
            actions.reverse()

            return actions

        for successor in problem.getSuccessors(current[0]):
            if successor[0] not in visited:
                queue.push(successor)
                parents[successor] = current
                visited.add(successor[0])
    return None


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    # here we are mixing the benefits of bfs and dfs
    # we are using a priority queue to keep track of the frontier
    pq = util.PriorityQueue()
    visited = set()

    pq.push((problem.getStartState(), list()), 0)

    while (not pq.isEmpty()):
        state, path = pq.pop()
        visited.add(state)

        if (problem.isGoalState(state)):
            return path

        for successor in problem.getSuccessors(state):
            if successor[0] not in visited:
                inFrontier = False
                for element in pq.heap:
                    if element[2][0] == successor[0]:
                        inFrontier = True
                        break

                newPath = path + [successor[1]]
                newCost = problem.getCostOfActions(newPath)

                if not inFrontier:
                    pq.push((successor[0], newPath), newCost)
                elif problem.getCostOfActions(element[2][1]) > newCost:
                    pq.update((successor[0], newPath), newCost)

    return None


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    # A* is a combination of UCS and heuristic
    pq = util.PriorityQueue()
    visited = set()

    pq.push((problem.getStartState(), list()),
            heuristic(problem.getStartState(), problem))

    while not pq.isEmpty():
        state, path = pq.pop()
        visited.add(state)

        if problem.isGoalState(state):
            return path

        for successor in problem.getSuccessors(state):
            if successor[0] not in visited:
                inFrontier = False
                for element in pq.heap:
                    if element[2][0] == successor[0]:
                        inFrontier = True
                        break

                hCost = heuristic(successor[0], problem)
                newPath = path + [successor[1]]
                newCost = problem.getCostOfActions(newPath)

                if not inFrontier:
                    pq.push((successor[0], newPath), newCost + hCost)
                elif problem.getCostOfActions(element[2][1]) > newCost:
                    pq.update((successor[0], newPath), newCost + hCost)

    return None


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
