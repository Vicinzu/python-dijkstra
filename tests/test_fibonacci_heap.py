import unittest
from typing import List, Tuple

from fibonacci_heap import *


class TestFibonacciHeap(unittest.TestCase):
    @staticmethod
    def __getFibonacciHeapTestData() -> List[Tuple[float, str]]:
        return [(10, 'Element 1'),
                (5, 'Element 2'),
                (20, 'Element 3'),
                (25, 'Element 4')]

    @staticmethod
    def __genFibonacciHeapTestData(num=10) -> List[Tuple[float, str]]:
        result: List[Tuple[float, str]] = []
        for i in range(num):
            result.append((i, 'Element '+str(i)))

        return result

    def __testElement(self, expectedElement: Tuple[float, str], receivedElement: FibonacciHeapNode[str]):
        self.assertEqual(expectedElement, self.__toTuple(receivedElement))

    @staticmethod
    def __toTuple(receivedElement: FibonacciHeapNode[str]) -> Tuple[float, str]:
        if receivedElement is None:
            return None

        return (receivedElement.getPriority(), receivedElement.getItem())

    def testFibonacciHeap_AddGetMin(self):
        fheap: FibonacciHeap = FibonacciHeap[str]()
        minElement: Tuple[float, str] = None
        self.assertEqual(len(fheap), 0)
        self.__testElement(minElement, fheap.getMin())

        element = minElement = (10, 'Element 1')
        fheap.add(*element)
        self.assertEqual(len(fheap), 1)
        self.__testElement(minElement, fheap.getMin())

        element = (20, 'Element 2')
        fheap.add(*element)
        self.assertEqual(len(fheap), 2)
        self.__testElement(minElement, fheap.getMin())

        element = minElement = (5, 'Element 3')
        fheap.add(*element)
        self.assertEqual(len(fheap), 3)
        self.__testElement(minElement, fheap.getMin())

    def testFibonacciHeap_AddExtractMin(self):
        fheap: FibonacciHeap = FibonacciHeap[str]()
        self.assertEqual(len(fheap), 0)
        testData: List[Tuple[float, object]] = self.__getFibonacciHeapTestData()

        fheap.add(*testData[0])
        self.assertEqual(len(fheap), 1)
        fheap.add(*testData[1])
        self.assertEqual(len(fheap), 2)
        fheap.add(*testData[2])
        self.assertEqual(len(fheap), 3)

        self.__testElement(testData[1], fheap.extractMin())
        self.assertEqual(len(fheap), 2)
        self.__testElement(testData[0], fheap.extractMin())
        self.assertEqual(len(fheap), 1)
        fheap.add(*testData[3])
        self.assertEqual(len(fheap), 2)
        self.__testElement(testData[2], fheap.extractMin())
        self.assertEqual(len(fheap), 1)
        self.__testElement(testData[3], fheap.extractMin())
        self.assertEqual(len(fheap), 0)
        self.__testElement(None, fheap.extractMin())

    def testFibonacciHeap_DecreasePriority_Normal(self):
        fheap: FibonacciHeap = FibonacciHeap[str]()
        testData: List[Tuple[float, str]] = self.__getFibonacciHeapTestData()
        testDataEntry: List[FibonacciHeapNode] = []
        for dataEntry in testData:
            testDataEntry.append(fheap.add(*dataEntry))
        self.assertEqual(len(fheap), 4)
        self.__testElement(testData[1], fheap.extractMin())

        # Test a decrease that does not change the tree
        fheap.decreaseKey(15, testDataEntry[2])
        self.__testElement(testData[0], fheap.getMin())

        # Test a decrease that changes the tree
        fheap.decreaseKey(8, testDataEntry[2])
        self.__testElement((8, testData[2][1]), fheap.getMin())

    def testFibonacciHeap_DecreasePriority_RecursiveCut(self):
        fheap: FibonacciHeap = FibonacciHeap[str]()
        testData: List[Tuple[float, str]] = self.__genFibonacciHeapTestData(10)
        testDataEntry: List[FibonacciHeapNode] = []
        for dataEntry in testData:
            testDataEntry.append(fheap.add(*dataEntry))
        self.assertEqual(len(fheap), 10)
        self.__testElement(testData[0], fheap.extractMin())

        # Ensure that a parent node is marked first and then cut as root
        fheap.decreaseKey(4, testDataEntry[6])
        fheap.decreaseKey(4, testDataEntry[7])

        # Test if the expected result
        self.__testElement(testData[1], fheap.extractMin())

    def testFibonacciHeap_Iterate(self):
        fheap: FibonacciHeap = FibonacciHeap[str]()

        # generate the test data
        numEntries: int = 10
        testData: List[Tuple[float, str]] = self.__genFibonacciHeapTestData(numEntries)

        # add the test data to the fibonacci heap
        for data in testData:
            fheap.add(*data)
        # test the number of elements in the heap
        self.assertEqual(len(fheap), numEntries)

        # test if the number of iterations (roots) is equal to the number of inserted nodes
        n: int = 0
        for root in fheap:
            n += 1
        self.assertEqual(len(fheap), n)

        # make a binomial tree of it
        fheap.extractMin()

        # get the smallest entry
        minNode: FibonacciHeapNode = fheap.getMin()

        # test if the number of iterations (children of node) is equal to the rank (length)
        n = 0
        for child in minNode:
            n += 1
        self.assertEqual(len(minNode), n)
