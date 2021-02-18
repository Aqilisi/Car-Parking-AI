This program places waiting cars inside a parking lot. It is just a fun project written in python.

Available methods: DFS, BFS, BestFS.

1.
First you set up an initial_state like:
initial_state = [number_of_cars, ['E', 'NO'], ['P1', 'NO'], ...]
In the number_of_cars you choose an integer number of cars waiting to get parked. You need at least one empty space 
(entrance) ['E', 'NO']. E stands for empty and NO stands for no car on it. Then you choose how many platforms do you want.
Remember they must be less that the available spaces minus the entrance.

2.
You choose a method between DFS, BFS, BestFS by writing it next to method = ... . For instance, method = "DFS" .

3. 
Run.

4.
The program will display for you the current front and queue for every step. _GOAL_FOUND_ means that all cars waiting
are successfully parked and _GOAL_FAILED_ that there are cars still waiting while the parking is full.