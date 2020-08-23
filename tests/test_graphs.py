import unittest
from math import inf
from typing import List

from dijkstra.graph import *
from dijkstra.graph.graph_util import _EdgeInputData, _GraphInputData


class TestGraphMatrix(unittest.TestCase):
    @staticmethod
    def generateTestGraphInputData() -> Graph:
        edges: List[_EdgeInputData] = []
        edges.append(_EdgeInputData(1, 2, 1))
        edges.append(_EdgeInputData(1, 3, 3))
        edges.append(_EdgeInputData(2, 3, 1))
        edges.append(_EdgeInputData(2, 4, 8))
        edges.append(_EdgeInputData(3, 4, 2))

        return GraphMatrix(_GraphInputData(4, 5, 1, 4, edges))

    def testGraph(self):
        graph: Graph = TestGraphMatrix.generateTestGraphInputData()
        self.assertEqual(graph.getNumVertex(), 4)
        self.assertEqual(graph.getNumEdge(), 5)
        self.assertEqual(graph.getStartVertexId(), 1)
        self.assertEqual(graph.getEndVertexId(), 4)
        self.assertEqual(graph.getWeight(1, 2), 1)
        self.assertEqual(graph.getWeight(2, 3), 1)
        self.assertEqual(graph.getWeight(3, 4), 2)
        self.assertEqual(graph.getWeight(1, 4), inf)
