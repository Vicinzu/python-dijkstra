from dataclasses import dataclass
from typing import List, NamedTuple


class InvalidInstanceError(Exception):
    pass


@dataclass
class _EdgeInputData:
    vertexFrom: int
    vertexTo: int
    weight: float

    def __init__(self, vertexFrom: int, vertexTo: int, weight: float):
        self.vertexFrom = int(vertexFrom)
        self.vertexTo = int(vertexTo)
        self.weight = float(weight)


class _GraphInputData(NamedTuple):
    numVertex: int
    numEdge: int
    startVertexId: int
    endVertexId: int
    edgeData: List[_EdgeInputData]


class _FileLineWrapper(object):
    def __init__(self, f):
        self.f = f
        self.line = 0

    def close(self):
        return self.f.close()

    def readline(self):
        currentLine = self.f.readline()
        if(currentLine):
            self.line += 1
        return currentLine
    # to allow using in 'with' statements

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        currentLine = self.readline()
        if currentLine:
            return currentLine
        else:
            raise StopIteration
