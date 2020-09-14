import unittest
from typing import Tuple

from fibonacci_heap import *


class TestFibonacciHeap(unittest.TestCase):
    @staticmethod
    def __getFibonacciHeapTestData() -> List[Tuple[float, object]]:
        return [(10, 'Element 1'), (5, 'Element 2'), (20, 'Element 3'), (25, 'Element 4')]

    def __testElement(self, gotElement: Tuple[float, object], expectedElement: Tuple[float, object]):
        self.assertEqual(expectedElement, gotElement)

    def testFibonacciHeap_AddGetMin(self):
        fheap: FibonacciHeap = FibonacciHeap()
        minElement: Tuple[float, object] = (inf, None)
        self.assertEqual(len(fheap), 0)
        self.__testElement(fheap.getMin(), minElement)

        element = minElement = (10, 'Element 1')
        fheap.add(*element)
        self.assertEqual(len(fheap), 1)
        self.__testElement(fheap.getMin(), minElement)

        element = (20, 'Element 2')
        fheap.add(*element)
        self.assertEqual(len(fheap), 2)
        self.__testElement(fheap.getMin(), minElement)

        element = minElement = (5, 'Element 3')
        fheap.add(*element)
        self.assertEqual(len(fheap), 3)
        self.__testElement(fheap.getMin(), minElement)

    def testFibonacciHeap_AddExtractMin(self):
        fheap: FibonacciHeap = FibonacciHeap()
        self.assertEqual(len(fheap), 0)
        testData: List[Tuple[float, object]] = self.__getFibonacciHeapTestData()

        fheap.add(*testData[0])
        self.assertEqual(len(fheap), 1)
        fheap.add(*testData[1])
        self.assertEqual(len(fheap), 2)
        fheap.add(*testData[2])
        self.assertEqual(len(fheap), 3)

        self.__testElement(fheap.extractMin(), testData[1])
        self.assertEqual(len(fheap), 2)
        self.__testElement(fheap.extractMin(), testData[0])
        self.assertEqual(len(fheap), 1)
        fheap.add(*testData[3])
        self.assertEqual(len(fheap), 2)
        self.__testElement(fheap.extractMin(), testData[2])
        self.assertEqual(len(fheap), 1)
        self.__testElement(fheap.extractMin(), testData[3])
        self.assertEqual(len(fheap), 0)
        self.__testElement(fheap.extractMin(), (inf, None))

    def testFibonacciHeap_DecreasePriority(self):
        fheap: FibonacciHeap = FibonacciHeap()
        testData: List[Tuple[float, object]] = self.__getFibonacciHeapTestData()

        fheap.add(*testData[0])
        self.assertEqual(len(fheap), 1)
        fheap.add(*testData[1])
        self.assertEqual(len(fheap), 2)

        self.__testElement(fheap.getMin(), testData[1])
        fheap.decreaseKey(2, *testData[0])
        self.__testElement(fheap.getMin(), (2, testData[0][1]))
