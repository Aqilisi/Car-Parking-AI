"""
----------------------------------
Authors:
Pappas Achilleas
@aqilisi
----------------------------------
"""

import copy
import sys
import time
import numpy as np

sys.setrecursionlimit(10 ** 6)

# The Parking Spaces Diagram
#
#   +-------+-------+-------+
#   |   6   |   5   |   4   |
#   +-------+-------+-------+
#   |   1   |   2   |   3   |
#   +-------+-------+-------+
#       ^
#    Entrance
#


''' Set the current number of parking spaces and the adjacency list. '''
''' Acceptable values: Entrance + at least 1 parking space '''


spaces = {
    1: [2, 6],
    2: [1, 5, 3],
    3: [2, 4],
    4: [3, 5],
    5: [2, 4, 6],
    6: [1, 5]
}

# The Parking Initial State Diagram
#
#   +-------+-------+-------+
#   | P5 NO | P4 NO | P3 NO |
#   +-------+-------+-------+
#   |   E   | P1 NO | P2 NO |
#   +-------+-------+-------+
#       ^
#   5 vehicles waiting
#


'''--------------------------------------------------------------------------------------------------------------'''
''' Check if there is an available platform at the antrance space. '''
''' If exists we load a car. '''


def enter(state):
    if state[0] != 0 and state[1][0][0] == 'P' and state[1][1] == 'NO':
        new_state = [state[0] - 1] + [[state[1][0], 'YES']] + state[2:]
        return new_state


'''--------------------------------------------------------------------------------------------------------------'''
''' Exchange positions. '''


def swap(state_l, i, j):
    state_l[i], state_l[j] = state_l[j], state_l[i]
    return state_l


'''--------------------------------------------------------------------------------------------------------------'''
''' First neighbour. Check the dictionary (spaces) and chooses the first neighbour. '''


def neighbour1(state):
    elem = ['E', 'NO']
    i = state.index(elem) if elem in state else -1
    if i >= 0:
        swap(state, i, spaces[i][0])
        return state


'''--------------------------------------------------------------------------------------------------------------'''
''' Second neighbour. Check the dictionary (spaces) and chooses the second neighbour, if exists. '''


def neighbour2(state):
    elem = ['E', 'NO']
    i = state.index(elem) if elem in state else -1
    if i >= 0 and len(spaces[i]) == 2:  # Check if the second neighbour exists
        swap(state, i, spaces[i][1])
        return state


'''--------------------------------------------------------------------------------------------------------------'''
''' Third neighbour. Check the dictionary (spaces) and chooses the third neighbour, if exists. '''


def neighbour3(state):
    elem = ['E', 'NO']
    i = state.index(elem) if elem in state else -1
    if i >= 0 and len(spaces[i]) == 3:  # Check if the third neighbour exists
        swap(state, i, spaces[i][2])
        return state


'''--------------------------------------------------------------------------------------------------------------'''
''' Forth neighbour. Check the dictionary (spaces) and chooses the forth neighbour, if exists. '''


def neighbour4(state):
    elem = ['E', 'NO']
    i = state.index(elem) if elem in state else -1
    if i >= 0 and len(spaces[i]) == 4:  # Check if the forth neighbour exists
        swap(state, i, spaces[i][3])
        return state  # The max number of neighbours is 4.


'''--------------------------------------------------------------------------------------------------------------'''
''' Find all nodes '''


def find_children(state):
    children = []

    enter_state = copy.deepcopy(state)
    enter_child = enter(enter_state)  # Check if a node is created by a car entering the parking.

    tr1_state = copy.deepcopy(state)
    tr1_child = neighbour1(tr1_state)  # Check if a node is created by the first neighbour.

    tr2_state = copy.deepcopy(state)
    tr2_child = neighbour2(tr2_state)  # Check if a node is created by the second neighbour.

    tr3_state = copy.deepcopy(state)
    tr3_child = neighbour3(tr3_state)  # Check if a node is created by the third neighbour.

    tr4_state = copy.deepcopy(state)
    tr4_child = neighbour4(tr4_state)  # Check if a node is created by the forth neighbour.

    # Place every new node at the end of children.

    if tr1_child is not None:
        children.append(tr1_child)

    if tr2_child is not None:
        children.append(tr2_child)

    if tr3_child is not None:
        children.append(tr3_child)

    if tr4_child is not None:
        children.append(tr4_child)

    if enter_child is not None:
        children.append(enter_child)

    return children


'''--------------------------------------------------------------------------------------------------------------'''
''' Create front. '''


def make_front(state):
    return [state]


'''--------------------------------------------------------------------------------------------------------------'''
''' Expand front. '''


def expand_front(front, method):
    if method == 'DFS':  # Check if we use DFS mode (Depth First Search).
        if front:
            print("Front:")
            print(front)
            node = front.pop(0)  # Remove the parent node and use it to generate children nodes.
            for child in find_children(node):  # find_children returns children nodes and we insert them
                front.insert(0, child)  # at the start of the front.

    elif method == 'BFS':  # Check if we use BFS mode (Breath First Search).
        if front:
            print("Front:")
            print(front)
            node = front.pop(0)  # Remove the parent node and use it to generate children nodes.
            for child in find_children(node):  # find_children returns children nodes and we insert them
                front.append(child)  # at the end of the front.

    elif method == 'BestFS':  # Check if we use BestFS mode (Best First Search).
        if front:
            print("Front:")
            print(front)
            node = front.pop(0)  # Remove the parent node and use it to generate children nodes.
            for child in find_children(node):  # find_children returns children nodes and we insert them
                front.append(child)  # at the end of the front.
            # Sorting all nodes in the front by the heuristic criteria.
            front = sort_front(front, node)

    return front


'''--------------------------------------------------------------------------------------------------------------'''
''' Sorting front '''


def sort_front(front, node): 
    distances = []  # Distance from goal for every node-child
    sorted_front = []  # List to store the sorted front
    
    # Check if a platform is at the entrance and if there are cars on it.  
    for count in range(len(front)):  # Repeat for every node contained in front
        platform = bool(front[count][1][0][0] == 'P')  # Check if a platform exists at the entrance
        parked = bool(front[count][1][1] == 'YES')  # Check if there is a car on the platform
        node_check = bool(node[1][1] == 'YES')  # Check if the parent node had a platform with a car on top

        # The heuristic criteria matches a child node with a calculated "distance"
        # The distance is calculated according to how close is a platform to load a car.
        # Examine if the newly created child has at the entrance:
        # 1. Platform with a car, it just loaded a car
        # 2. Empty
        # 3. Platform without car

        if platform and parked:
            if node_check:
                distances.append(4)  # If the parent node has loaded a car and at the next step
                # the platform is still at the same place and full then
                # we assign the biggest possible distance
            else:
                distances.append(1)  # Assign the smallest possible distance to the newer child created by loading a car
        elif not platform:
            distances.append(2)  # Assign distance if there is not a platform on entrance
        elif platform and not parked:
            distances.append(3)  # Assign distance if there is a platform on entrance without a car loaded

    temp_array = np.array(distances)  # Create a numpy array which contains all the calculated distances
    sorted_distances_indexes = np.argsort(temp_array)  # The np.argsort returns an array that contains the
    # sorted indexes of all distances.

    for i in sorted_distances_indexes:
        sorted_front.append(front[i])  # Depending of the indexes, sort the front.

    return sorted_front


'''--------------------------------------------------------------------------------------------------------------'''
''' Queue creation. '''


def make_queue(state):
    return [[state]]


'''--------------------------------------------------------------------------------------------------------------'''
''' Extend queue. '''


def extend_queue(queue, method):
    if method == 'DFS':  # Check if we use DFS mode (Depth First Search)
        print("Queue:")
        print(queue)
        node = queue.pop(0)  # Remove the parent node και and use it to generate children nodes.
        queue_copy = copy.deepcopy(queue)
        children = find_children(node[-1])  # find_children returns children nodes and we insert them
        for child in children:  # at the start of the front.
            path = copy.deepcopy(node)
            path.append(child)
            queue_copy.insert(0, path)

    elif method == 'BFS':  # Check if we use BFS mode (Breath First Search).
        print("Queue:")
        print(queue)
        node = queue.pop(0)
        queue_copy = copy.deepcopy(queue)
        children = find_children(node[-1])  # Remove the parent node and use it to generate children nodes
        for child in children:  
            path = copy.deepcopy(node)
            path.append(child) # Add them to the end of the queue.
            queue_copy.append(path)

    elif method == 'BestFS':  # Check if we use BFS mode (Breath First Search).
        print("Queue:")
        print(queue)
        node = queue.pop(0)
        queue_copy = copy.deepcopy(queue)
        children = find_children(node[-1])  # Remove the parent node και and use it to generate children nodes.
        for child in children:  
            path = copy.deepcopy(node)
            path.append(child) # Add them to the end of the queue.
            queue_copy.append(path)
    # Sorting all nodes in the front by the heuristic criteria.
    queue_copy = sort_queue(queue_copy, node)

    return queue_copy


'''--------------------------------------------------------------------------------------------------------------'''
''' Sorting queue. '''


def sort_queue(queue, node):
    distances = []  # Distance from goal for every node-child
    sorted_queue = []  # List to store the sorted queue

    # Check if a platform is at the entrance and if there are cars on it. 
    for count in range(len(queue)):  # Repeat for every node contained in queue
        platform = bool(queue[count][-1][1][0][0] == 'P')  # Check if a platform exists at the entrance
        parked = bool(queue[count][-1][1][1] == 'YES')  # Check if there is a car on the platform
        node_check = bool(node[0][1][1] == 'YES')  # Check if the parent node had a platform with a car on top

        # The heuristic criteria matches a child node with a calculated "distance"
        # The distance is calculated according to how close is a platform to load a car.
        # Examine if the newly created child has at the entrance:
        # 1. Platform with a car, it just loaded a car
        # 2. Empty
        # 3. Platform without car

        if platform and parked:
            if node_check:
                distances.append(4)  # If the parent node has loaded a car and at the next step
                # the platform is still at the same place and full then
                # we assign the biggest possible distance
            else:
                distances.append(1)  # Assign the smallest possible distance to the newer child created by loading a car
        elif not platform:
            distances.append(2)   # Assign distance if there is not a platform on entrance
        elif platform and not parked:
            distances.append(3)  # Assign distance if there is a platform on entrance without a car loaded

    temp_array = np.array(distances)  # Create a numpy array which contains all the calculated distances
    sorted_distances_indexes = np.argsort(temp_array)  # The np.argsort returns an array that contains the
    # sorted indexes of all distances.

    for i in sorted_distances_indexes:
        sorted_queue.append(queue[i])  # Depending of the indexes, sort the queue

    return sorted_queue


'''--------------------------------------------------------------------------------------------------------------'''
''' Check front and search for a solution, reject a node or express inability to find a solution. '''


def find_solution(front, queue, closed, method):
    if not front:  # Check if there are nodes left in front.
        print('_NO_SOLUTION_FOUND_')  # If front is empty then we have no solution.

    elif front[0] in closed:  # Check if the firt node of front is contained in closed sum.
        new_front = copy.deepcopy(front)
        new_front.pop(0)  # Remove the node we already checked.
        new_queue = copy.deepcopy(queue)
        new_queue.pop(0)  # Remove from the queue the route of the node we checked.
        find_solution(new_front, new_queue, closed, method)

    elif is_goal_state(front[0]):  # Checks if current node is a solution.
        print('_GOAL_FOUND_')
        print("Front:")
        print(front[0])
        print("Queue:")
        print(queue)

    else:
        closed.append(front[0])  # Place the current node that we are going to check in the closed sum.
        front_copy = copy.deepcopy(front)
        front_children = expand_front(front_copy, method)  # We extend the front.
        queue_copy = copy.deepcopy(queue)
        queue_children = extend_queue(queue_copy, method)  # We extend the queue.
        closed_copy = copy.deepcopy(closed)
        find_solution(front_children, queue_children, closed_copy, method)


'''--------------------------------------------------------------------------------------------------------------'''
''' Check if the current front is a solution. '''


def is_goal_state(front):
    return bool(front[0] == 0)  # If no cars are waiting returns true else returns false.


'''--------------------------------------------------------------------------------------------------------------'''
''' Main function. '''


def main():
    # Set initial state manual.
    initial_state = [4, ['E', 'NO'], ['P1', 'NO'], ['P2', 'NO'], ['P3', 'NO'], ['P4', 'NO'], ['P5', 'NO']]

    # Choose method manualy (DFS, BFS, BestFS).
    method = "BestFS"

    # Start timer.
    start_time = time.time()

    # Start searching.
    print('____BEGIN__SEARCHING____')
    find_solution(make_front(initial_state), make_queue(initial_state), [], method)

    # Display execution time.
    print('____Time elapsed:____')
    print((time.time() - start_time), 'seconds')  # Time elapsed.


'''--------------------------------------------------------------------------------------------------------------'''
''' Program start. '''


if __name__ == "__main__":
    main()
