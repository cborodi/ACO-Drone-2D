from random import *

import numpy
import pygame

from utils import *
import numpy as np

from ant import *

class AntColonyOptimization():
    def __init__(self, distanceMatrix):
        self.graph = distanceMatrix
        self.numberOfSensors = len(self.graph)
        self.numberOfAnts = NUMBER_OF_ANTS
        self.trails = np.zeros((self.numberOfSensors, self.numberOfSensors))
        self.probabilities = [0.0] * self.numberOfSensors

        self.ants = []

        for i in range(self.numberOfAnts):
            self.ants.append(Ant(self.numberOfSensors))

        # from utils
        self.iterations = ITERATIONS
        self.q0 = Q0
        self.Q = Q
        self.rho = RHO
        self.alpha = ALPHA
        self.beta = BETA

        self.c = C
        self.currentIndex = -1
        self.bestTourOrder = []
        self.bestTourLength = -1

    def run(self):
        for i in range(self.iterations):
            self.solve()
        return self.bestTourLength, self.bestTourOrder

    def solve(self):
        self.setUpAnts()
        self.clearTrails()
        for i in range(self.numberOfSensors - 1):
            self.moveAnts()
        self.updateBest()

    def moveAnts(self):
        for ant in self.ants:
            x = self.selectNextCity(ant)
            ant.visitSensor(self.currentIndex, x)
            self.trails[ant.trail[self.currentIndex]][x] *= self.rho
            self.trails[ant.trail[self.currentIndex]][x] += 1 / self.graph[ant.trail[self.currentIndex]][x]
            self.trails[x][ant.trail[self.currentIndex]] = self.trails[ant.trail[self.currentIndex]][x]
        self.currentIndex += 1

    def selectNextCity(self, ant):
        x = random()
        if x < self.q0:
            toVisit = -1
            arg = -1
            for sensor in range(self.numberOfSensors):
                if ant.checkVisited(sensor) is False:
                    if self.trails[ant.trail[self.currentIndex]][sensor] ** ALPHA * (1 / self.graph[ant.trail[self.currentIndex]][sensor]) ** BETA > arg:
                        arg = self.trails[ant.trail[self.currentIndex]][sensor] ** ALPHA * (1 / self.graph[ant.trail[self.currentIndex]][sensor]) ** BETA
                        toVisit = sensor
            return toVisit
        else:
            self.computeProbabilities(ant)
            r = random()
            total = 0.0
            for i in range(self.numberOfSensors):
                total += self.probabilities[i]
                if total >= r:
                    return i

    def computeProbabilities(self, ant):
        pheromone = 0.0
        for sensor in range(self.numberOfSensors):
            if ant.checkVisited(sensor) is False:
                pheromone += self.trails[ant.trail[self.currentIndex]][sensor] ** ALPHA * (1 / self.graph[ant.trail[self.currentIndex]][sensor]) ** BETA
        for sensor in range(self.numberOfSensors):
            if ant.checkVisited(sensor):
                self.probabilities[sensor] = 0.0
            else:
                numerator = self.trails[ant.trail[self.currentIndex]][sensor] ** ALPHA * (1 / self.graph[ant.trail[self.currentIndex]][sensor]) ** BETA
                self.probabilities[sensor] = numerator / pheromone

    def updateBest(self):
        if self.bestTourOrder == []:
            self.bestTourOrder = self.ants[0].trail
            self.bestTourLength = self.ants[0].trailLength(self.graph)
        for ant in self.ants:
            if ant.trailLength(self.graph) < self.bestTourLength:
                self.bestTourLength = ant.trailLength(self.graph)
                self.bestTourOrder = ant.trail.copy()

    def setUpAnts(self):
        for ant in self.ants:
            ant.clear()
            ant.visitSensor(-1, SENSORS) # visit the drone
        self.currentIndex = 0

    def clearTrails(self):
        for i in range(self.numberOfSensors):
            for j in range(self.numberOfSensors):
                self.trails[i][j] = self.c
        if self.bestTourLength > -1:
            for i in range(len(self.bestTourOrder) - 1):
                self.trails[i][i+1] += 1 / self.bestTourLength
