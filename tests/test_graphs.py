import unittest
from math import inf
from typing import List, Tuple

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

    def testGraphMatrix_GetWeight(self):
        graph: Graph = TestGraphMatrix.generateTestGraphInputData()
        self.assertEqual(graph.getNumVertex(), 4)
        self.assertEqual(graph.getNumEdge(), 5)
        self.assertEqual(graph.getStartVertexId(), 1)
        self.assertEqual(graph.getEndVertexId(), 4)
        self.assertEqual(graph.getWeight(1, 2), 1)
        self.assertEqual(graph.getWeight(2, 3), 1)
        self.assertEqual(graph.getWeight(3, 4), 2)
        self.assertEqual(graph.getWeight(1, 4), inf)

    def containsEdge(self, edges:List[Tuple[int, float]], toVertexId:int, weight:float) -> bool:
        self.assertEqual(edges.count((toVertexId,weight)), 1, 'Does not contain the edge to {} with weight {}.'.format(toVertexId, weight))

    def testGraphMatrix_GetEdges(self):
        graph: Graph = TestGraphMatrix.generateTestGraphInputData()
        edges:List[Tuple[int, float]] = graph.getEdges(1)
        self.assertEqual(len(edges), 2)
        self.containsEdge(edges, 2, 1)
        self.containsEdge(edges, 3, 3)
        edges = graph.getEdges(4)
        self.assertEqual(len(edges), 0, 'Edge to 4 should not be contained.')
