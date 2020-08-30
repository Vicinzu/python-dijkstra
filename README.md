# python-dijkstra
## Description
This implementation of the dijkstra algorithm is based on python. It was motivated by the need of having a goal for training my python skills.

## Unit-Tests
The unit-tests can be found in the folder *tests*. Each module has its own test-file.

## Test-Instances
Six different instances, coded as text-files, can be found in the corresponding sub-folder.

### Format
  Row | Format | Meaning
  --- | ------ | -------
  1st | Integer | Number of Vertices  
  2nd | Integer | Number of Edges  
  3rd | Integer | Origin Vertex  
  4th | Integer | Target Vertex  
  5th+ | Integer : Integer : Float | Edge &rarr; Begin Vertex : End Vertex : Weight

### Solutions
Instance | Optimal Costs | Optimal Path
-------- | ------------ | -------------
input.txt.1 | 4 | 1, 2, 3, 4
input.txt.2 | 16 | 1, 2, 5, 9, 10
input.txt.3 | 16 | 1, 2, 5, 9, 10
input.txt.100 | 122 | 1, 48, 4, 26, 100
input.txt.200 | 50800 | 1, 60, 173, 200
input.txt.1000 | 69 | 1, 121, 724, 304, 879, 552, 102, 1000
