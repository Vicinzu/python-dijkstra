from math import inf
from typing import List

from dijkstra.distance import Distance
from dijkstra.graph import Graph

from .frontier import Frontier


class FrontierList(Frontier):
    __numVertex: int
    __distances: Distance
    __elements: List[int]

    def __init__(self, graph: Graph, distances: Distance):
        if graph is None:
            raise ValueError('Invalid graph.')
        elif distances is None:
            raise ValueError('Invalid distances.')

        self.__numVertex = graph.getNumVertex()
        self.__elements = []
        self.__distances = distances

    def addVertex(self, vertexId: int):
        if vertexId is None or vertexId < 1 or vertexId > self.__numVertex:
            raise ValueError('Invalid vertexId: {}'.format(vertexId))

        self.__elements.append(vertexId)

    def getLength(self) -> int:
        return len(self.__elements)

    def isEmpty(self) -> bool:
        return not self.__elements

    def removeVertex(self, vertexId: int) -> bool:
        if vertexId is None or vertexId < 1 or vertexId > self.__numVertex:
            raise ValueError('Invalid vertexId: {}'.format(vertexId))

        try:
            self.__elements.remove(vertexId)
        except ValueError:
            pass

    def getMinDistanceVertex(self) -> (int, float):
        minDistanceVertexId: int = None
        minDistance: float = inf

        for v in self.__elements:
            distance: float = self.__distances.getDistance(v)
            if distance < minDistance:
                minDistanceVertexId = v
                minDistance = distance

        return (minDistanceVertexId, minDistance)

    def diminishDistance(self, vertexId: int, oldDistance: float, newDistance: float):
        if vertexId is None or vertexId < 1 or vertexId > self.__numVertex:
            raise ValueError('Invalid vertexId: {}'.format(vertexId))
        elif newDistance is None:
            raise ValueError('Invalid distance.')

        self.__distances.setDistance(vertexId, newDistance)


class FrontierBuckets(Frontier):
    __numVertex: int
    __maxDistance: int
    __buckets: List[List[int]]
    __distances: Distance
    __lastMinDistBucket: int

    def __init__(self, graph: Graph, distances: Distance):
        if graph is None:
            raise ValueError('Invalid graph.')
        elif distances is None:
            raise ValueError('Invalid distances.')

        self.__numVertex = graph.getNumVertex()
        self.__maxDistance = self.__getMaxWeight(graph) + 1
        self.__buckets = [[] for b in range(self.__maxDistance)]
        self.__distances = distances
        self.__lastMinDistBucket = 0

    @staticmethod
    def __getMaxWeight(graph: Graph) -> int:
        maxWeight: int = -inf
        for n in range(1, graph.getNumVertex()):
            for toVertexId, weight in graph.getEdges(n):
                if weight > maxWeight:
                    maxWeight = weight
        return int(maxWeight)

    def addVertex(self, vertexId: int):
        distance: int = int(self.__distances.getDistance(vertexId))
        bucketId: int = distance % self.__maxDistance

        try:
            self.__buckets[bucketId].index(vertexId)
        except ValueError:
            self.__buckets[bucketId].append(vertexId)

    def removeVertex(self, vertexId: int):
        distance: int = int(self.__distances.getDistance(vertexId))
        bucketId: int = distance % self.__maxDistance

        try:
            self.__buckets[distance % self.__maxDistance].remove(vertexId)
        except ValueError:
            pass

    def getLength(self) -> int:
        result: int = 0
        for bucket in self.__buckets:
            result += len(bucket)

        return result

    def isEmpty(self) -> bool:
        return self.getLength() == 0

    def getMinDistanceVertex(self) -> (int, float):
        i: int = 0
        while not self.__buckets[(self.__lastMinDistBucket+i) % self.__maxDistance] and i < self.__maxDistance:
            i = i+1

        if i == self.__maxDistance:
            return (None, inf)
        else:
            self.__lastMinDistBucket = (
                self.__lastMinDistBucket+i) % self.__maxDistance
            vertexId: int = self.__buckets[self.__lastMinDistBucket][0]
            return vertexId, self.__distances.getDistance(vertexId)

    def diminishDistance(self, vertexId: int, oldDistance: float, newDistance: float):
        self.__distances.setDistance(vertexId, newDistance)
        if oldDistance != inf:
            self.__buckets[int(oldDistance) %
                           self.__maxDistance].remove(vertexId)
        self.__buckets[int(newDistance) % self.__maxDistance].append(vertexId)
