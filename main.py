from parser import Parser as p
from classes import Graph, Zone


data = p.parse_file("small_ex.txt")
graph = p.build_graph(data)
print([zone.connections for zone in graph.zones])
