import unittest
from math import inf

from dijkstra.predecessor import *
from tests.test_graphs import Graph, getTestGraphInstance


class TestPredecessorList(unittest.TestCase):
    @staticmethod
    def generatePredecessorTestData() -> Predecessor:
        g: Graph = getTestGraphInstance()
        p: Predecessor = PredecessorList(g)
        p.setPredecessor(2, 1)
        p.setPredecessor(3, 2)
        return p

    def testPredecessorList_Get(self):
        predecessors: Predecessor = self.generatePredecessorTestData()
        self.assertEqual(predecessors.getPredecessor(1), None)
        self.assertEqual(predecessors.getPredecessor(2), 1)
        self.assertEqual(predecessors.getPredecessor(3), 2)

    def testPredecessorList_Set(self):
        predecessors: Predecessor = self.generatePredecessorTestData()
        # Assign new predecessor for vertex with already known predecessor
        self.assertEqual(predecessors.getPredecessor(3), 2)
        predecessors.setPredecessor(3, 1)
        self.assertEqual(predecessors.getPredecessor(3), 1)
        # Assign new predecessor for vertex with still unknown predecessor
        self.assertEqual(predecessors.getPredecessor(4), None)
        predecessors.setPredecessor(4, 2)
        self.assertEqual(predecessors.getPredecessor(4), 2)
