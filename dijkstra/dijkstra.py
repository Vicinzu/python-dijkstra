from typing import List

from dijkstra.graph import *
from dijkstra.predecessor import *
from dijkstra.distance import *
from dijkstra.frontier import *

@dataclass
class DijkstraSolution:
    costs: float
    path: List[int]

class Dijkstra:
    __graph: Graph
    __predecessors: Predecessor
    __distances: Distance
    __frontier: Frontier

    def __init__(self, instanceFilePath: string):
        self.__graph = GraphMatrix(instanceFilePath)
        self.__predecessors = PredecessorList(self.__graph)
        self.__distances = DistanceList(self.__graph)
        self.__frontier = FrontierList(self.__graph, self.__distances)

    def run(self):
        while(not self.__frontier.isEmpty()):
            # get next minimum vertex
            minDistanceVertex: (int, float) = self.__frontier.getMinDistanceVertex()
            currentVertexId: int = minDistanceVertex[0]

            # remove minimum vertex from frontier
            self.__frontier.removeVertex(currentVertexId)

            edges:List[Tuple[int, float]] = self.__graph.getEdges(currentVertexId)
            for (toVertexId, weight) in edges:
                self.analyzeNewEdge(minDistanceVertex[1], toVertexId, weight)

        #TODO Provisorial.
        print('Solution from {} to {} with distnace {}.'.format(self.__graph.getStartVertexId(), self.__graph.getEndVertexId(), self.__distances.getDistance(self.__graph.getStartVertexId())))

    def analyzeNewEdge(self, currentVertexId:int, currentDistance:float, toVertexId:int, weight:float):
        newDistance = currentDistance + weight
        oldDistance = self.__distances.getDistance(toVertexId)
        if newDistance < oldDistance:
            self.__predecessors.setPredecessor(currentVertexId)
            self.__frontier.diminishDistance(toVertexId, oldDistance, newDistance)
            self.__frontier.addVertex(toVertexId)

    def getSolution(self) -> DijkstraSolution:
        #TODO Missing implementation.
        pass