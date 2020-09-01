from dijkstra import *

instanceFile: str = './instances/input.txt.1000'
d: Dijkstra = Dijkstra(instanceFile)
d.run()

print('Instance \'{}\':'.format(instanceFile))
if(d.hasSolution()):
    solution: DijkstraSolution = d.getSolution()
    print('A solution with a distance of {} has been found. It took {:.4f} ms.\nPath: {}'.format(
        solution.distance, solution.duration, solution.getFormatedPath()))
else:
    print('No solution has been found.')
