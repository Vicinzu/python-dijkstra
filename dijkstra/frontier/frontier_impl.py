from math import inf
from typing import List

from dijkstra.distance import Distance
from dijkstra.graph import Graph
from fibonacci_heap import *

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
    
    def __len__(self) -> int:
        return len(self.__elements)

    def addVertex(self, vertexId: int):
        if vertexId is None or vertexId < 1 or vertexId > self.__numVertex:
            raise ValueError('Invalid vertexId: {}'.format(vertexId))

        self.__elements.append(vertexId)

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

    def __len__(self) -> int:
        result: int = 0
        for bucket in self.__buckets:
            result += len(bucket)

        return result

    def addVertex(self, vertexId: int):
        distance: int = int(self.__distances.getDistance(vertexId))
        bucketId: int = distance % self.__maxDistance

        try:
            self.__buckets[bucketId].index(vertexId)
        except ValueError:
            self.__buckets[bucketId].append(vertexId)

    def removeVertex(self, vertexId: int):
        if vertexId is None or vertexId < 1 or vertexId > self.__numVertex:
            raise ValueError('Invalid vertexId: {}'.format(vertexId))

        distance: int = int(self.__distances.getDistance(vertexId))
        bucketId: int = distance % self.__maxDistance

        try:
            self.__buckets[distance % self.__maxDistance].remove(vertexId)
        except ValueError:
            pass

    def isEmpty(self) -> bool:
        return len(self) == 0

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
        if vertexId is None or vertexId < 1 or vertexId > self.__numVertex:
            raise ValueError('Invalid vertexId: {}'.format(vertexId))
        elif newDistance is None:
            raise ValueError('Invalid distance.')

        self.__distances.setDistance(vertexId, newDistance)
        if oldDistance != inf:
            self.__buckets[int(oldDistance) %
                           self.__maxDistance].remove(vertexId)
        self.__buckets[int(newDistance) % self.__maxDistance].append(vertexId)


class FrontierFibonacci(Frontier):
    __graph: Graph
    __distances: Distance
    __heap: FibonacciHeap[int]
    __heapNodes: List[FibonacciHeapNode]

    def __init__(self, graph: Graph, distances: Distance):
        if graph is None:
            raise ValueError('Invalid graph.')
        elif distances is None:
            raise ValueError('Invalid distances.')

        self.__graph = graph
        self.__distances = distances
        self.__heap = FibonacciHeap()
        self.__heapNodes = [None for n in range(graph.getNumVertex())]

    def __len__(self) -> int:
        return len(self.__heap)

    def addVertex(self, vertexId: int):
        if vertexId is None or vertexId < 1 or vertexId > self.__graph.getNumVertex():
            raise ValueError('Invalid vertexId: {}'.format(vertexId))

        if self.__getNode(vertexId) is None:
            distance: int = int(self.__distances.getDistance(vertexId))
            self.__heapNodes[vertexId-1] = self.__heap.add(distance, vertexId)

    def removeVertex(self, vertexId: int):
        if vertexId is None or vertexId < 1 or vertexId > self.__graph.getNumVertex():
            raise ValueError('Invalid vertexId: {}'.format(vertexId))

        if vertexId == self.__heap.getMin().getItem():
            self.__heap.extractMin()
        else:
            raise NotImplementedError('Currently only the minimum can be removed.')

    def isEmpty(self) -> bool:
        return len(self) == 0

    def getMinDistanceVertex(self) -> (int, float):
        if self.isEmpty():
            return (None, inf)

        result: FibonacciHeapNode[int] = self.__heap.getMin()
        return (result.getItem(), result.getPriority())

    def diminishDistance(self, vertexId: int, oldDistance: float, newDistance: float):
        if vertexId is None or vertexId < 1 or vertexId > self.__graph.getNumVertex():
            raise ValueError('Invalid vertexId: {}'.format(vertexId))
        elif newDistance is None:
            raise ValueError('Invalid distance.')

        node: FibonacciHeapNode[int] = self.__getNode(vertexId)
        if node is not None:
            self.__heap.decreaseKey(newDistance, node)

        self.__distances.setDistance(vertexId, newDistance)

    def __getNode(self, vertexId: int):
        return self.__heapNodes[vertexId-1]

    def __isNodeInFrontier(self, vertexId: int):
        return self.__getNode(vertexId) is not None
