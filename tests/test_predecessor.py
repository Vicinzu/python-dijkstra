import unittest
from abc import ABC, abstractmethod
from math import inf

from dijkstra.predecessor import *
from tests.test_graphs import Graph, TestGraphList


class TestPredecessorGeneral(ABC):
    @classmethod
    @abstractmethod
    def _initPredecessorImpl(cls, graph: Graph) -> Predecessor:
        pass

    @classmethod
    def __setPredecessorTestData(cls, predecessor: Predecessor):
        predecessor.setPredecessor(2, 1)
        predecessor.setPredecessor(3, 2)

    @classmethod
    def getTestDistanceInstance(cls) -> Predecessor:
        graph: Graph = TestGraphList.getTestGraphInstance()
        predecessor: Predecessor = cls._initPredecessorImpl(graph)
        cls.__setPredecessorTestData(predecessor)
        return predecessor

    def testPredecessor_Get(self):
        predecessors: Predecessor = self.getTestDistanceInstance()
        self.assertEqual(predecessors.getPredecessor(1), None)
        self.assertEqual(predecessors.getPredecessor(2), 1)
        self.assertEqual(predecessors.getPredecessor(3), 2)

    def testPredecessor_Set(self):
        predecessors: Predecessor = self.getTestDistanceInstance()
        # Assign new predecessor for vertex with already known predecessor
        self.assertEqual(predecessors.getPredecessor(3), 2)
        predecessors.setPredecessor(3, 1)
        self.assertEqual(predecessors.getPredecessor(3), 1)
        # Assign new predecessor for vertex with still unknown predecessor
        self.assertEqual(predecessors.getPredecessor(4), None)
        predecessors.setPredecessor(4, 2)
        self.assertEqual(predecessors.getPredecessor(4), 2)


class TestPredecessorList(TestPredecessorGeneral, unittest.TestCase):
    @classmethod
    def _initPredecessorImpl(cls, graph: Graph) -> Predecessor:
        return PredecessorList(graph)
