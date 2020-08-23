from abc import ABC, abstractmethod

from dijkstra.graph import Graph


class Distance(ABC):
    @abstractmethod
    def __init__(self, graph: Graph):
        pass

    @abstractmethod
    def getDistance(self, vertexId: int) -> float:
        pass

    @abstractmethod
    def setDistance(self, vertexId: int, distance: float):
        pass
