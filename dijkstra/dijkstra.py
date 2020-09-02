import time
from dataclasses import dataclass
from math import inf
from typing import List, Tuple

from dijkstra.distance import *
from dijkstra.frontier import *
from dijkstra.graph import *
from dijkstra.predecessor import *


@dataclass
class DijkstraSolution:
    distance: float
    path: Tuple[int]
    duration: float

    def __init__(self):
        self.distance = inf
        self.path = []
        self.duration = 0

    def getFormatedPath(self) -> str:
        if not self.path:
            return ''

        return ' -> '.join(map(str, self.path))


class Dijkstra:
    __graph: Graph
    __predecessors: Predecessor
    __distances: Distance
    __frontier: Frontier
    __duration: time

    def __init__(self, instanceFilePath: str):
        self.__graph = GraphList(instanceFilePath)
        self.__predecessors = PredecessorList(self.__graph)
        self.__distances = DistanceList(self.__graph)
        self.__frontier = FrontierBuckets(self.__graph, self.__distances)
        self.__duration = 0

    def run(self):
        startTime = time.time()
        self.__distances.setDistance(self.__graph.getStartVertexId(), 0)
        self.__frontier.addVertex(self.__graph.getStartVertexId())
        while(not self.__frontier.isEmpty()):
            # get next minimum vertex
            (currentVertexId, currentDistance) = self.__frontier.getMinDistanceVertex()

            # remove minimum vertex from frontier
            self.__frontier.removeVertex(currentVertexId)

            edges: List[Tuple[int, float]] = self.__graph.getEdges(
                currentVertexId)
            for (toVertexId, weight) in edges:
                self.__analyzeNewEdge(
                    currentVertexId, currentDistance, toVertexId, weight)

        self.__duration = (time.time() - startTime)*1000

    def hasSolution(self):
        return self.__distances.getDistance(self.__graph.getEndVertexId()) < inf

    def getSolution(self) -> DijkstraSolution:
        solution: DijkstraSolution = DijkstraSolution()

        if self.hasSolution():
            solution.distance = self.__distances.getDistance(
                self.__graph.getEndVertexId())
            solution.path = self.__getPath()
            solution.duration = self.__duration

        return solution

    def __analyzeNewEdge(self, currentVertexId: int, currentDistance: float, toVertexId: int, weight: float):
        newDistance = currentDistance + weight
        oldDistance = self.__distances.getDistance(toVertexId)
        if newDistance < oldDistance:
            self.__predecessors.setPredecessor(toVertexId, currentVertexId)
            self.__frontier.diminishDistance(
                toVertexId, oldDistance, newDistance)
            self.__frontier.addVertex(toVertexId)

    def __getPath(self) -> Tuple[int]:
        result: List[int] = []
        currentNode: int = self.__graph.getEndVertexId()
        while currentNode:
            result.insert(0, currentNode)
            currentNode = self.__predecessors.getPredecessor(currentNode)

        # if no path has been found (only end node is in list), then return an empty list
        if len(result) == 1:
            result.clear()

        return tuple(result)
