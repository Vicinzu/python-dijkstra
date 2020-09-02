import unittest
from abc import ABC, abstractmethod
from math import inf
from typing import List, Tuple

from dijkstra.graph import *
from dijkstra.graph.graph_util import _EdgeInputData, _GraphInputData


class _TestGraphGeneral(ABC):
    @classmethod
    def __generateTestGraphInputData(cls) -> _GraphInputData:
        edges: List[_EdgeInputData] = []
        edges.append(_EdgeInputData(1, 2, 1))
        edges.append(_EdgeInputData(1, 3, 3))
        edges.append(_EdgeInputData(2, 3, 1))
        edges.append(_EdgeInputData(2, 4, 8))
        edges.append(_EdgeInputData(3, 4, 2))
        return _GraphInputData(4, 5, 1, 4, edges)

    @classmethod
    @abstractmethod
    def _initGraphImpl(cls, graphInputData: _GraphInputData) -> Graph:
        pass

    @classmethod
    def getTestGraphInstance(cls) -> Graph:
        data: _GraphInputData = cls.__generateTestGraphInputData()
        return cls._initGraphImpl(data)

    def testGraph_GetWeight(self):
        graph: Graph = self.getTestGraphInstance()
        self.assertEqual(graph.getNumVertex(), 4)
        self.assertEqual(graph.getNumEdge(), 5)
        self.assertEqual(graph.getStartVertexId(), 1)
        self.assertEqual(graph.getEndVertexId(), 4)
        self.assertEqual(graph.getWeight(1, 2), 1)
        self.assertEqual(graph.getWeight(2, 3), 1)
        self.assertEqual(graph.getWeight(3, 4), 2)
        self.assertEqual(graph.getWeight(1, 4), inf)

    def __containsEdge(self, edges: List[Tuple[int, float]], toVertexId: int, weight: float) -> bool:
        self.assertEqual(edges.count((toVertexId, weight)), 1,
                         'Does not contain the edge to {} with weight {}.'.format(toVertexId, weight))

    def testGraph_GetEdges(self):
        graph: Graph = self.getTestGraphInstance()
        edges: List[Tuple[int, float]] = graph.getEdges(1)
        self.assertEqual(len(edges), 2)
        self.__containsEdge(edges, 2, 1)
        self.__containsEdge(edges, 3, 3)
        edges = graph.getEdges(4)
        self.assertEqual(len(edges), 0, 'Edge to 4 should not be contained.')


class TestGraphMatrix(_TestGraphGeneral, unittest.TestCase):
    @classmethod
    def _initGraphImpl(cls, graphInputData: _GraphInputData) -> Graph:
        return GraphMatrix(graphInputData)


class TestGraphList(_TestGraphGeneral, unittest.TestCase):
    @classmethod
    def _initGraphImpl(cls, graphInputData: _GraphInputData) -> Graph:
        return GraphList(graphInputData)
