from math import inf
from typing import List

from dijkstra.distance import Distance
from dijkstra.graph import Graph

from .frontier import Frontier


class FrontierList(Frontier):
    __numVertex: int
    __distances:Distance
    __elements:List[int]

    def __init__(self, graph:Graph, distances:Distance):
        if graph is None:
            raise ValueError('Invalid graph.')
        elif distances is None:
            raise ValueError('Invalid distances.')
        
        self.__numVertex=graph.getNumVertex()
        self.__elements=[]
        self.__elements.append(graph.getStartVertexId())
        self.__distances=distances

    def addVertex(self, vertexId:int):
        if vertexId is None or vertexId<1 or vertexId>self.__numVertex:
            raise ValueError('Invalid vertexId: {}'.format(vertexId))

        self.__elements.append(vertexId)

    def getLength(self) -> int:
        return len(self.__elements)

    def isEmpty(self) -> bool:
        return not self.__elements

    def removeVertex(self, vertexId:int) -> bool:
        if vertexId is None or vertexId<1 or vertexId>self.__numVertex:
            raise ValueError('Invalid vertexId: {}'.format(vertexId))

        try:
            self.__elements.remove(vertexId)
        except ValueError:
            pass

    def getMinDistanceVertex(self) -> (int, float):
        minDistanceVertexId:int=None
        minDistance:float=inf

        for v in self.__elements:
            distance:float = self.__distances.getDistance(v)
            if distance<minDistance:
                minDistanceVertexId=v
                minDistance=distance
        
        return (minDistanceVertexId, minDistance)

    def diminishDistance(self, vertexId:int, oldDistance:float, newDistance:float):
        if vertexId is None or vertexId<1 or vertexId>self.__numVertex:
            raise ValueError('Invalid vertexId: {}'.format(vertexId))
        elif newDistance is None:
            raise ValueError('Invalid distance.')

        self.__distances.setDistance(vertexId, newDistance)
