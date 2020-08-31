from abc import ABC, abstractmethod

from dijkstra.distance import Distance
from dijkstra.graph import Graph


class Frontier(ABC):
    @abstractmethod
    def __init__(self, graph: Graph, distances: Distance):
        pass

    @abstractmethod
    def addVertex(self, vertexId: int):
        pass

    @abstractmethod
    def removeVertex(self, vertexId: int):
        pass

    @abstractmethod
    def getLength(self) -> int:
        pass

    @abstractmethod
    def isEmpty(self) -> bool:
        pass

    @abstractmethod
    def getMinDistanceVertex(self) -> (int, float):
        pass

    @abstractmethod
    def diminishDistance(self, vertexId: int, oldDistance: float, newDistance: float):
        pass
