import unittest
from math import inf

from dijkstra.distance import *
from tests.test_graphs import Graph, getTestGraphInstance


class TestDistanceList(unittest.TestCase):
    @staticmethod
    def generateDistanceTestData() -> Distance:
        g: Graph = getTestGraphInstance()
        d: Distance = DistanceList(g)
        d.setDistance(1, 0)
        d.setDistance(2, 2)
        d.setDistance(3, 2.5)
        return d

    def testDistanceList_get(self):
        distances: Distance = self.generateDistanceTestData()
        self.assertEqual(distances.getDistance(1), 0)
        self.assertEqual(distances.getDistance(2), 2)
        self.assertEqual(distances.getDistance(3), 2.5)
        self.assertEqual(distances.getDistance(4), inf)

    def testDistanceList_set(self):
        distances: Distance = self.generateDistanceTestData()
        # Assign new distance for vertex with finate weight
        self.assertEqual(distances.getDistance(2), 2)
        distances.setDistance(2, 1)
        self.assertEqual(distances.getDistance(2), 1)
        # Assign new distance for vertex with infinate weight
        self.assertEqual(distances.getDistance(4), inf)
        distances.setDistance(4, 2)
        self.assertEqual(distances.getDistance(4), 2)
