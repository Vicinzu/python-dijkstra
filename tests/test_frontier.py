import unittest
from math import inf

from dijkstra.distance import *
from dijkstra.frontier import *
from tests.test_graphs import TestGraphMatrix



class TestFrontierList(unittest.TestCase):
    @staticmethod
    def generateFrontierTestData() -> Frontier:
        g: graph = TestGraphMatrix.generateTestGraphInputData()
        d: Distance = DistanceList(g)
        d.setDistance(2,1)
        d.setDistance(3,2)
        d.setDistance(4,3)
        f: Frontier = FrontierList(g, d)

        return f

    def assertMinDistance(self, frontier, expectedVertexId, expectedDistance):
        minDistanceVertex:(int,float)=frontier.getMinDistanceVertex()
        self.assertEqual(minDistanceVertex[0],expectedVertexId)
        self.assertEqual(minDistanceVertex[1],expectedDistance)

    def testDistanceList_Length(self):
        frontier: Frontier = self.generateFrontierTestData()
        self.assertEqual(frontier.getLength(),1)

    def testDistanceList_Length(self):
        frontier: Frontier = self.generateFrontierTestData()
        self.assertEqual(frontier.isEmpty(),False)
        frontier.removeVertex(1)
        self.assertEqual(frontier.isEmpty(),True)

    def testDistanceList_Add(self):
        frontier: Frontier = self.generateFrontierTestData()
        self.assertEqual(frontier.getLength(),1)        
        frontier.addVertex(2)
        self.assertEqual(frontier.getLength(),2)

    def testDistanceList_Remove(self):
        frontier: Frontier = self.generateFrontierTestData()
        self.assertEqual(frontier.getLength(),1)        
        frontier.removeVertex(1)
        self.assertEqual(frontier.getLength(),0)

    def testDistanceList_MinDistance(self):
        frontier: Frontier = self.generateFrontierTestData()
        self.assertMinDistance(frontier, 1, 0)
        frontier.removeVertex(1)
        self.assertMinDistance(frontier, None, inf)
        frontier.addVertex(2)
        self.assertMinDistance(frontier, 2, 1)

    def testDistanceList_DecreaseDistance(self):
        frontier: Frontier = self.generateFrontierTestData()
        frontier.removeVertex(1)
        frontier.addVertex(4)
        self.assertMinDistance(frontier, 4, 3)
        frontier.diminishDistance(4, 3, 2)
        self.assertMinDistance(frontier, 4, 2)


        