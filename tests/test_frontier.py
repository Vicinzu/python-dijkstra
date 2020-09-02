import unittest
from abc import ABC, abstractmethod
from math import inf

from dijkstra.distance import *
from dijkstra.frontier import *
from tests.test_graphs import Graph, TestGraphList


class TestFrontierGeneral(ABC):
    @classmethod
    def __setDistancesTestData(cls, distances: Distance):
        distances.setDistance(1, 0)
        distances.setDistance(2, 1)
        distances.setDistance(3, 2)
        distances.setDistance(4, 3)

    @classmethod
    @abstractmethod
    def _initFrontierImpl(cls, graph: Graph, distances: Distance) -> Frontier:
        pass

    @classmethod
    def getTestFrontierInstance(cls) -> Frontier:
        graph = TestGraphList.getTestGraphInstance()
        distances = DistanceList(graph)
        cls.__setDistancesTestData(distances)
        return cls._initFrontierImpl(graph, distances)

    def testFrontier_Length(self):
        frontier: Frontier = self.getTestFrontierInstance()
        self.assertEqual(frontier.getLength(), 0)
        frontier.addVertex(1)
        self.assertEqual(frontier.getLength(), 1)

    def testFrontier_Length(self):
        frontier: Frontier = self.getTestFrontierInstance()
        self.assertEqual(frontier.isEmpty(), True)
        frontier.addVertex(1)
        self.assertEqual(frontier.isEmpty(), False)

    def testFrontier_Add(self):
        frontier: Frontier = self.getTestFrontierInstance()
        self.assertEqual(frontier.getLength(), 0)
        frontier.addVertex(1)
        self.assertEqual(frontier.getLength(), 1)

    def testFrontier_Remove(self):
        frontier: Frontier = self.getTestFrontierInstance()
        frontier.addVertex(1)
        self.assertEqual(frontier.getLength(), 1)
        frontier.removeVertex(1)
        self.assertEqual(frontier.getLength(), 0)

    def __assertMinDistance(self, frontier, expectedVertexId, expectedDistance):
        minDistanceVertex: (int, float) = frontier.getMinDistanceVertex()
        self.assertEqual(minDistanceVertex[0], expectedVertexId)
        self.assertEqual(minDistanceVertex[1], expectedDistance)

    def testFrontier_MinDistance(self):
        frontier: Frontier = self.getTestFrontierInstance()
        self.__assertMinDistance(frontier, None, inf)
        frontier.addVertex(3)
        self.__assertMinDistance(frontier, 3, 2)
        frontier.removeVertex(3)
        frontier.addVertex(2)
        self.__assertMinDistance(frontier, 2, 1)

    def testFrontier_DecreaseDistance(self):
        frontier: Frontier = self.getTestFrontierInstance()
        frontier.addVertex(4)
        self.__assertMinDistance(frontier, 4, 3)
        frontier.diminishDistance(4, 3, 2)
        self.__assertMinDistance(frontier, 4, 2)


class TestFrontierList(TestFrontierGeneral, unittest.TestCase):
    @classmethod
    def _initFrontierImpl(cls, graph: Graph, distances: Distance) -> Frontier:
        return FrontierList(graph, distances)


class TestFrontierBuckets(TestFrontierGeneral, unittest.TestCase):
    @classmethod
    def _initFrontierImpl(cls, graph: Graph, distances: Distance) -> Frontier:
        return FrontierBuckets(graph, distances)
