import unittest
from math import inf

from dijkstra.predecessor import *
from tests.test_graphs import TestGraphMatrix


class TestPredecessorList(unittest.TestCase):
    @staticmethod
    def generatePredecessorTestData() -> Predecessor:
        g: graph = TestGraphMatrix.generateTestGraphInputData()
        p: Predecessor = PredecessorList(g)
        p.setPredecessor(2, 1)
        p.setPredecessor(3, 2)
        return p

    def testDistanceGetSet(self):
        predecessors: Predecessor = self.generatePredecessorTestData()
        self.assertEqual(predecessors.getPredecessor(1), None)
        self.assertEqual(predecessors.getPredecessor(2), 1)
        self.assertEqual(predecessors.getPredecessor(3), 2)
