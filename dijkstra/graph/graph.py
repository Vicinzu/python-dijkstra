import errno
import os.path
from abc import ABC, abstractmethod
from typing import List, Tuple

from .graph_util import *
from .graph_util import _FileLineWrapper, _EdgeInputData, _GraphInputData


class Graph(ABC):
    @abstractmethod
    def __init__(self, filename:str):
        pass

    @abstractmethod
    def __init__(self, graphData:_GraphInputData):
        pass

    @abstractmethod
    def getNumVertex(self) -> int:
        pass

    @abstractmethod
    def getNumEdge(self) -> int:
        pass

    @abstractmethod
    def getStartVertexId(self) -> int:
        pass

    @abstractmethod
    def getEndVertexId(self) -> int:
        pass

    @abstractmethod
    def getWeight(self, fromVertexId, toVertexId) -> float:
        pass

    @abstractmethod
    def getEdges(self, fromVertexId) -> List[Tuple[int, float]]:
        pass

    @staticmethod
    def _readFile(filePath:str) -> _GraphInputData:
        """Reads an instance text file and returns an internal data structure.

        Args:
            filePath (str): the path to the instance file

        Raises:
            FileNotFoundError: Raised when the instance file does not exist
            InvalidInstanceError: Raised when the instance does not seem to be consistent.

        Returns:
            _GraphInputData: an internal data structure containing the graph represented by the instance file.
        """
        if not os.path.isfile(filePath):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filePath)
        
        file:_FileLineWrapper = _FileLineWrapper(open(filePath,'r'))
        try:
            numVertex = int(file.readline())
            if numVertex <=1:
                raise InvalidInstanceError('The graph has to contain at least 1 vertex.')
            numEdges = int(file.readline())
            if numEdges<0:
                raise InvalidInstanceError('Invalid number of edges.')
            startVertex = int(file.readline())
            endVertex = int(file.readline())
            if startVertex<1 or startVertex>numVertex or endVertex<1 or endVertex>numVertex:
                raise InvalidInstanceError('Invalid start and/or end vertex-id.')

            edges:List[_EdgeInputData]=[]
            for line in (x.strip() for x in file):
                if line:
                    ed = _EdgeInputData(*line.split(':'))
                    if ed.vertexFrom<1 or ed.vertexFrom>numVertex or ed.vertexTo<1 or ed.vertexTo>numVertex:
                        raise InvalidInstanceError('Invalid start and/or end vertex-id for edge on line {}.'.format(file.line))
                    edges.append(ed)
            if(numEdges!=len(edges)):
                raise InvalidInstanceError('There were {} edges specified, but {} have been defined.'.format(numEdges, len(edges)))

            file.close()

            return _GraphInputData(numVertex, numEdges, startVertex, endVertex, edges)
        except ValueError:
            file.close()
            raise InvalidInstanceError('Line {} contains non-cumeric data.'.format(file.line))
        except InvalidInstanceError as iie:
            file.close()
            raise iie
