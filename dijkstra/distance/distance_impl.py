from math import inf
from typing import List

from dijkstra.graph import Graph

from .distance import Distance


class DistanceList(Distance):
    __numVertex: int
    __distances: List[int]

    def __init__(self, graph: Graph):
        if graph is None:
            raise ValueError('Invalid graph.')

        self.__numVertex = graph.getNumVertex()
        self.__distances = [inf for p in range(graph.getNumVertex())]
        self.setDistance(graph.getStartVertexId(), 0)

    def getDistance(self, vertexId: int) -> int:
        if vertexId is None or vertexId < 1 or vertexId > self.__numVertex:
            raise ValueError('Invalid vertexId: {}'.format(vertexId))

        return self.__distances[vertexId-1]

    def setDistance(self, vertexId: int, distance: float):
        if vertexId is None or vertexId < 1 or vertexId > self.__numVertex:
            raise ValueError('Invalid vertexId: {}'.format(vertexId))
        elif distance is None:
            raise ValueError('Invalid distance.')

        self.__distances[vertexId-1] = distance
