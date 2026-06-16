from parser import Parser as p
from classes import Graph, Zone


data = p.parse_file("example.txt")
graph = p.build_graph(data)
for zone in graph.zones:
    print(f"={zone.name}:")
    for k, v in zone.neighbors.items():
        print("     ", v[0].name, v[1].max_link_capacity)
for drone in graph.drones:
    print(drone.id)
    print("--", drone.position.name)
