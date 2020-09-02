import unittest
from abc import ABC, abstractmethod
from math import inf

from dijkstra.distance import *
from tests.test_graphs import Graph, TestGraphList


class TestDistanceGeneal(ABC):
    @classmethod
    @abstractmethod
    def _initDistanceImpl(cls, graph: Graph) -> Distance:
        pass

    @classmethod
    def __setDistancesTestData(cls, distances: Distance):
        distances.setDistance(1, 0)
        distances.setDistance(2, 2)
        distances.setDistance(3, 2.5)

    @classmethod
    def getTestDistanceInstance(cls) -> Distance:
        graph: Graph = TestGraphList.getTestGraphInstance()
        distances: Distance = cls._initDistanceImpl(graph)
        cls.__setDistancesTestData(distances)
        return distances

    def testDistance_Get(self):
        distances: Distance = self.getTestDistanceInstance()
        self.assertEqual(distances.getDistance(1), 0)
        self.assertEqual(distances.getDistance(2), 2)
        self.assertEqual(distances.getDistance(3), 2.5)
        self.assertEqual(distances.getDistance(4), inf)

    def testDistance_Set(self):
        distances: Distance = self.getTestDistanceInstance()
        # Assign new distance for vertex with finate weight
        self.assertEqual(distances.getDistance(2), 2)
        distances.setDistance(2, 1)
        self.assertEqual(distances.getDistance(2), 1)
        # Assign new distance for vertex with infinate weight
        self.assertEqual(distances.getDistance(4), inf)
        distances.setDistance(4, 2)
        self.assertEqual(distances.getDistance(4), 2)


class TestDistanceList(TestDistanceGeneal, unittest.TestCase):
    @classmethod
    def _initDistanceImpl(cls, graph: Graph) -> Distance:
        return DistanceList(graph)
