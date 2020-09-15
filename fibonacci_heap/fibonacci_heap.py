from dataclasses import dataclass
from math import ceil, inf, log
from typing import Generic, TypeVar

FibonacciHeapNodeItemType = TypeVar('FibonacciHeapNodeItemType')


class FibonacciHeapNode(Generic[FibonacciHeapNodeItemType]):
    _priority: float
    _item: FibonacciHeapNodeItemType
    _parent: 'FibonacciHeapNode'
    _firstChild: 'FibonacciHeapNode'
    _leftSibling: 'FibonacciHeapNode'
    _rightSibling: 'FibonacciHeapNode'
    _rank: int
    _mark: bool

    def __init__(self, priority: float, item: FibonacciHeapNodeItemType = None):
        self._priority = priority
        self._item = item
        self._parent = None
        self._firstChild = None
        self._leftSibling = self
        self._rightSibling = self
        self._rank = 0
        self._mark = False

    def __str__(self):
        parentName = ''
        if self._parent is not None:
            parentName = self._parent._item
        return 'FibonacciHeapNode(priority={:d}, item={}, rank={:d}, mark={}, parent={})'.format(self._priority, self._item, self._rank, self._mark, parentName)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return _FibonacciHeapNodeIterator(self)

    def __len__(self):
        return self._rank

    def getPriority(self):
        return self._priority

    def getItem(self):
        return self._item


class FibonacciHeap(Generic[FibonacciHeapNodeItemType]):
    _root: FibonacciHeapNode
    _minNode: FibonacciHeapNode
    _length: int

    def __init__(self):
        self._root = None
        self._minNode = None
        self._length = 0

    def __str__(self):
        result: str = ''
        for rootNode in self:
            result += self.__printNode(rootNode)
        return result

    @classmethod
    def __printNode(cls, node: FibonacciHeapNode, level: int = 0) -> str:
        result: str = '{:=2d}:\t'.format(level)+"\t"*level+str(node)+"\n"
        for childnode in node:
            result += cls.__printNode(childnode, level+1)

        return result

    def __iter__(self):
        return _FibonacciHeapIterator(self)

    def __len__(self):
        return self._length

    def add(self, priority: float, item: FibonacciHeapNodeItemType = None) -> FibonacciHeapNode[FibonacciHeapNodeItemType]:
        newnode: FibonacciHeapNode = FibonacciHeapNode(priority, item)
        self.__add_nodes_as_roots(newnode)
        if self._minNode == None or newnode._priority <= self._minNode._priority:
            self._minNode = newnode
        self._length += 1

        return newnode

    def getMin(self) -> FibonacciHeapNode[FibonacciHeapNodeItemType]:
        return self._minNode

    def extractMin(self) -> FibonacciHeapNode[FibonacciHeapNodeItemType]:
        result: FibonacciHeapNode[FibonacciHeapNodeItemType] = self._minNode
        if result is not None:
            self.__cutoff_node(result)
            self.__add_nodes_as_roots(result._firstChild)
            self._length -= 1
            self._minNode = None
            self.__cleanup_roots()

        return result

    def decreaseKey(self, new_priority: float, node: FibonacciHeapNode[FibonacciHeapNodeItemType]):
        node._priority = new_priority
        self.__update_min(node)

        parent: FibonacciHeapNode = node._parent
        if parent is not None and parent._priority > node._priority:
            self.__cutoff_node(node)
            self.__add_nodes_as_roots(node)
            self.__cutoff_node_recursive(parent)

    def __update_min(self, node: FibonacciHeapNode[FibonacciHeapNodeItemType]):
        if self._minNode is None or self._minNode._priority > node._priority:
            self._minNode = node

    def __add_nodes_as_roots(self, newRoot: FibonacciHeapNode[FibonacciHeapNodeItemType]):
        if newRoot is None:
            return

        newRoot._parent = None
        if(self._root is None):
            self._root = newRoot
        else:
            currentLastElement:  FibonacciHeapNode = self._root._leftSibling
            self._root._leftSibling = newRoot._leftSibling
            newRoot._leftSibling._rightSibling = self._root
            newRoot._leftSibling = currentLastElement
            currentLastElement._rightSibling = newRoot

    def __cleanup_roots(self):
        if self._root is None:
            return

        maxRank: int = 1+ceil(2*log(self._length))
        sortField: List[FibonacciHeapNode[FibonacciHeapNodeItemType]] = [None for f in range(maxRank)]
        while self._root is not None:
            currentRoot: FibonacciHeapNode[FibonacciHeapNodeItemType] = self._root
            currentRank: int = currentRoot._rank
            self.__cutoff_node(currentRoot)
            self.__update_min(currentRoot)
            while sortField[currentRank] is not None:
                currentRoot = self.__link_nodes(currentRoot, sortField[currentRank])
                sortField[currentRank] = None
                currentRank += 1
            sortField[currentRank] = currentRoot
        for r in range(maxRank):
            if sortField[r] is not None:
                self.__add_nodes_as_roots(sortField[r])

    def __add_node_as_child(self, parent: FibonacciHeapNode[FibonacciHeapNodeItemType], child: FibonacciHeapNode[FibonacciHeapNodeItemType]):
        if parent._firstChild is None:
            parent._firstChild = child
            child._parent = parent
        else:
            firstChild: FibonacciHeapNode[FibonacciHeapNodeItemType] = parent._firstChild
            lastChild: FibonacciHeapNode[FibonacciHeapNodeItemType] = firstChild._leftSibling

            lastChild._rightSibling = child
            child._leftSibling = lastChild
            child._rightSibling = firstChild
            firstChild._leftSibling = child

        parent._rank += 1

    def __cutoff_node(self, node: FibonacciHeapNode[FibonacciHeapNodeItemType]):
        hasSibling: bool = node._rightSibling != node
        # If the node has a parent, then some data has to be corrected
        if node._parent is not None:
            # Decrease the rank of the parent
            node._parent._rank -= 1
            # Update the child pointer
            if node._parent._firstChild == node:
                if hasSibling:
                    node._parent._firstChild = node._rightSibling
                else:
                    node._parent._firstChild = None
            node._parent = None
        # The root pointer has to be updated, if it marks the node to cut
        elif self._root == node:
            if node._rightSibling == node:
                self._root = None
            else:
                self._root = node._rightSibling

        # if the element has siblings, then cut the element off the sibling list
        if hasSibling:
            _rightSibling = node._rightSibling
            _rightSibling._leftSibling = node._leftSibling
            node._leftSibling._rightSibling = _rightSibling
            node._leftSibling = node._rightSibling = node

    def __cutoff_node_recursive(self, node: FibonacciHeapNode):
        if node is not None:
            if node._mark == True:
                self.__cutoff_node(node)
                self.__add_nodes_as_roots(node)
                self.__cutoff_node_recursive(node._parent)
            else:
                node._mark = True

    def __link_nodes(self, leftTree: FibonacciHeapNode[FibonacciHeapNodeItemType], rightTree: FibonacciHeapNode[FibonacciHeapNodeItemType]) -> FibonacciHeapNode[FibonacciHeapNodeItemType]:
        parent: FibonacciHeapNode[FibonacciHeapNodeItemType] = leftTree
        child: FibonacciHeapNode[FibonacciHeapNodeItemType] = leftTree
        if rightTree._priority < leftTree._priority:
            parent = rightTree
        else:
            child = rightTree

        self.__add_node_as_child(parent, child)
        child._mark = False
        return parent


class _FibonacciHeapNodeIterator:
    __firstElement: FibonacciHeapNode
    __currentElement: FibonacciHeapNode
    __run: bool

    def __init__(self, fibonacciHeapNode: FibonacciHeapNode):
        self.__firstElement = fibonacciHeapNode._firstChild
        self.__currentElement = self.__firstElement
        self.__run = False

    def __next__(self):
        if self.__firstElement is None or (self.__run and self.__currentElement == self.__firstElement):
            raise StopIteration

        result = self.__currentElement
        self.__currentElement = self.__currentElement._rightSibling
        self.__run = True
        return result


class _FibonacciHeapIterator:
    __firstElement: FibonacciHeapNode
    __currentElement: FibonacciHeapNode
    __run: bool

    def __init__(self, fibonacciHeap: FibonacciHeap):
        self.__firstElement = fibonacciHeap._root
        self.__currentElement = self.__firstElement
        self.__run = False

    def __next__(self):
        if self.__currentElement is None or (self.__run and self.__currentElement == self.__firstElement):
            raise StopIteration

        result = self.__currentElement
        self.__currentElement = self.__currentElement._rightSibling
        self.__run = True
        return result
