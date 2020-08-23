from abc import ABC, abstractmethod

from dijkstra.graph import Graph


class Predecessor(ABC):
    @abstractmethod
    def __init__(self, graph: Graph):
        pass

    @abstractmethod
    def getPredecessor(self, vertexId: int) -> int:
        pass

    @abstractmethod
    def setPredecessor(self, vertexId: int, predecessorVertexId: int):
        pass
