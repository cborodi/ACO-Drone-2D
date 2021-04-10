# ACO-Drone-2D

A drone is placed in a known environment, described on a rectangular map of size n x n units, with the task to charge with energy k sensors. The sensors are placed in known positions, sensor i is at [xi, yi] onthe map. We want to charge these sensors as effectively as possible in order to use them to survey the maxim total area surrounding them. The drone moves and charges the sensors until it depletes its m units of energy from the battery. A sensor i can be charged with energy ei from the drone with a value from 0 to 5 (energy that comes from the drone’s battery), meaning that for a quantity of q energy it can see q squares around if there is no wall.
Using ACO (and any other suitable method <<A* used in this situation>>), write and complete the application that will be used in order to drive the drone in solving it’s task.


After computing the minimum distances between sensors and the paths, the problem reduces to a Travelling Salesman Problem in a complete graph.


The graphical user interface is implemented using the pygame module.
