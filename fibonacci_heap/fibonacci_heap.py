from dataclasses import dataclass
from math import inf
from typing import List, Tuple


@dataclass
class _FibonacciNode:
    priority: float
    item: object
    parent: '_FibonacciNode'
    firstChild: '_FibonacciNode'
    leftSibling: '_FibonacciNode'
    rightSibling: '_FibonacciNode'
    rank: int
    mark: bool

    def __init__(self, priority: float, item: object = None, parent: '_FibonacciNode' = None):
        self.priority = priority
        self.item = item
        self.parent = parent
        self.firstChild = None
        self.leftSibling = self
        self.rightSibling = self
        self.rank = 0
        self.mark = False


class FibonacciHeap:
    __root: _FibonacciNode
    __minNode: _FibonacciNode
    __length: int

    def __init__(self):
        self.__root = None
        self.__minNode = None
        self.__length = 0

    def __len__(self):
        return self.__length

    def add(self, priority: float, item: object = None):
        newTreeNode: _FibonacciNode = _FibonacciNode(priority, item)
        self.__merge_into_root(newTreeNode)
        if self.__minNode == None or newTreeNode.priority <= self.__minNode.priority:
            self.__minNode = newTreeNode
        self.__length += 1

    def getMin(self) -> Tuple[float, object]:
        if self.__minNode == None:
            return (inf, None)

        return (self.__minNode.priority, self.__minNode.item)

    def extractMin(self) -> Tuple[float, object]:
        if self.__minNode == None:
            return (inf, None)

        result: Tuple[float, object] = (self.__minNode.priority, self.__minNode.item)
        self.__cut_out_root(self.__minNode)
        self.__set_new_min()
        self.__length -= 1
        return result

    def decreaseKey(self, new_priority: float, old_priority: float, item: object = None):
        treeNode: _FibonacciNode = self.__find_key_value_internal(self.__root, old_priority, item)

        if treeNode is not None:
            treeNode.priority = new_priority
            if(treeNode.parent is not None and treeNode.parent.priority > new_priority):
                self.__cut_out_node(treeNode)
                self.__merge_into_root(treeNode)
            if treeNode.priority < self.__minNode.priority:
                self.__minNode = treeNode

    def __find_key_value(self, priority: float, item: object = None) -> _FibonacciNode:
        return self.__find_key_value_internal(self.__root, priority, item)

    def __find_key_value_internal(self, startNode: _FibonacciNode, priority: float, item: object = None) -> _FibonacciNode:
        result = None

        if startNode is not None:
            currentNode: _FibonacciNode = startNode
            while True:
                if currentNode.priority == priority and currentNode.item == item:
                    result = currentNode
                elif currentNode.priority < priority:
                    result = self.__find_key_value_internal(currentNode, priority, item)

                if result is not None or currentNode.rightSibling == self.__root:
                    break
                else:
                    currentNode = currentNode.rightSibling

        return result

    def __set_new_min(self):
        self.__minNode = self.__root
        if(self.__root is None):
            return

        currentNode: _FibonacciNode = self.__root
        while not currentNode.rightSibling == self.__root:
            currentNode = currentNode.rightSibling
            if currentNode.priority <= self.__root.priority:
                self.__minNode = currentNode

    def __merge_trees(self, leftTreeRoot: _FibonacciNode, rightTreeRoot: _FibonacciNode):
        rightTreeRoot.leftSibling = leftTreeRoot.leftSibling
        rightTreeRoot.rightSibling = leftTreeRoot
        leftTreeRoot.leftSibling.rightSibling = rightTreeRoot
        leftTreeRoot.leftSibling = rightTreeRoot

    def __merge_into_root(self, newTreeRoot: _FibonacciNode):
        if(self.__root is None):
            self.__root = newTreeRoot
        else:
            self.__merge_trees(self.__root, newTreeRoot)

    def __add_children_as_roots(self, treeRoot: _FibonacciNode):
        firstChild: _FibonacciNode = treeRoot.firstChild
        if firstChild is not None:
            treeRoot.rightSibling.leftSibling = firstChild.leftSibling
            firstChild.leftSibling.rightSibling = treeRoot
            firstChild.leftSibling = treeRoot
            treeRoot.rightSibling = firstChild
            firstChild.parent = None

    def __cut_out_node(self, treeNode: _FibonacciNode):
        if not treeNode.rightSibling == treeNode:
            rightSibling = treeNode.rightSibling
            rightSibling.leftSibling = treeNode.leftSibling
            treeNode.leftSibling.rightSibling = rightSibling
            treeNode.leftSibling = treeNode.rightSibling = treeNode

    def __cut_out_root(self, treeRoot: _FibonacciNode):
        if self.__root == treeRoot:
            if treeRoot.rightSibling == treeRoot:
                self.__root = None
            else:
                self.__root = treeRoot.rightSibling

        self.__add_children_as_roots(treeRoot)
        self.__cut_out_node(treeRoot)
