from typing import List

from dijkstra.graph import Graph

from .predecessor import Predecessor


class PredecessorList(Predecessor):
    __numVertex: int
    __predecessors: List[int]

    def __init__(self, graph: Graph):
        if graph is None:
            raise ValueError('Invalid graph.')

        self.__numVertex = graph.getNumVertex()
        self.__predecessors = [None for p in range(graph.getNumVertex())]

    def getPredecessor(self, vertexId: int) -> int:
        if vertexId is None or vertexId < 1 or vertexId > self.__numVertex:
            raise ValueError('Invalid vertexId: {}'.format(vertexId))

        return self.__predecessors[vertexId-1]

    def setPredecessor(self, vertexId: int, predecessorVertexId: int):
        if vertexId is None or vertexId < 1 or vertexId > self.__numVertex:
            raise ValueError('Invalid vertexId: {}'.format(vertexId))
        elif predecessorVertexId is None or predecessorVertexId < 1 or predecessorVertexId > self.__numVertex:
            raise ValueError(
                'Invalid predecessorVertexId: {}'.format(predecessorVertexId))

        self.__predecessors[vertexId-1] = predecessorVertexId
