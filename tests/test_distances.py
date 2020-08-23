import unittest
from math import inf

from dijkstra.distance import *
from tests.test_graphs import TestGraphMatrix


class TestDistanceList(unittest.TestCase):
    @staticmethod
    def generateDistanceTestData() -> Distance:
        g: graph = TestGraphMatrix.generateTestGraphInputData()
        d: Distance = DistanceList(g)
        d.setDistance(1, 0)
        d.setDistance(2, 2)
        return d

    def testDistanceGetSet(self):
        distances: Distance = self.generateDistanceTestData()
        self.assertEqual(distances.getDistance(1), 0)
        self.assertEqual(distances.getDistance(2), 2)
        self.assertEqual(distances.getDistance(3), inf)
