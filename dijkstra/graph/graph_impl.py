from math import inf
from typing import List, Tuple

from .graph import Graph
from .graph_util import _GraphInputData


class GraphMatrix(Graph):
    __numVertex:int
    __numEdge:int
    __startVertexId:int
    __endVertexId:int
    __weightMatrix:List[List[float]]

    def __init__(self, input:str):
        graphData:_GraphInputData
        if(isinstance(input, str)):
            super()._readFile(input)
        elif isinstance(input, _GraphInputData):
            graphData=input
        else:
            ValueError('Invalid input data.')

        self.__initWithData(graphData)

    def __initWithData(self, graphData:_GraphInputData):
        self.__numVertex=graphData.numVertex
        self.__numEdge=graphData.numEdge
        self.__startVertexId=graphData.startVertexId
        self.__endVertexId=graphData.endVertexId
        self.__weightMatrix = [[inf for i in range(graphData.numVertex)] for j in range(graphData.numVertex)]
        for ed in graphData.edgeData:
            self.__weightMatrix[ed.vertexFrom-1][ed.vertexTo-1]=ed.weight

    def getNumVertex(self) -> int:
        return self.__numVertex

    def getNumEdge(self) -> int:
        return self.__numEdge

    def getStartVertexId(self) -> int:
        return self.__startVertexId

    def getEndVertexId(self) -> int:
        return self.__endVertexId

    def getWeight(self, fromVertexId, toVertexId) -> float:
        if fromVertexId is None or fromVertexId<1 or fromVertexId>self.__numVertex:
            raise ValueError('Invalid fromVertexId: {}'.format(fromVertexId))
        elif toVertexId is None or toVertexId<1 or toVertexId>self.__numVertex:
            raise ValueError('Invalid toVertexId: {}'.format(toVertexId))

        return self.__weightMatrix[fromVertexId-1][toVertexId-1]

    def getEdges(self, fromVertexId) -> List[Tuple[int, float]]:
        if fromVertexId is None or fromVertexId<1 or fromVertexId>self.__numVertex:
            raise ValueError('Invalid fromVertexId: {}'.format(fromVertexId))

        results:List[(int, float)] = []
        for toVertexId, weight in enumerate(self.__weightMatrix[fromVertexId-1]):
            if weight < inf:
                results.append((toVertexId+1, weight))

        return results

