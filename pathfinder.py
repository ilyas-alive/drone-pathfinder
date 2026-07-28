from collections import deque
from classes import Graph, ZoneType

class PathFinder:
    def __init__(self, graph: Graph):
        self.graph = graph

    def compute_costs(self):
        costs = {self.graph.end_hub.name: 0.0}
        queue = deque([self.graph.end_hub.name])

        while queue:
            curr = queue.popleft()
            zone = self.graph.get_zone(curr)
            for n_name, (neighbor, _) in zone.neighbors.items():
                if n_name not in costs and neighbor.zone_type != ZoneType.BLOCKED:
                    costs[n_name] = costs[curr] + 1.0
                    queue.append(n_name)
        return costs
