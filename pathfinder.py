from classes import Graph, Zone, ZoneType
import heapq


class PathFinder:
    def __init__(self, graph: Graph) -> None:
        self.graph: Graph = graph

    def get_cost(self, zone: Zone) -> float:
        costs = {ZoneType.RESTRICTED: 2.0, ZoneType.PRIORITY: 0.5}
        return costs.get(zone.zone_type, 1.0)

    def compute_costs(self) -> dict[str, float]:
        if not self.graph.end_hub:
            raise ValueError("Graph has no end_hub")

        costs: dict[str, float] = {}
        heap: list[tuple[float, str]] = [(0.0, self.graph.end_hub.name)]

        while heap:
            cost, zone_name = heapq.heappop(heap)
            if zone_name in costs:
                continue

            costs[zone_name] = cost
            zone = self.graph.get_zone(zone_name)
            for n_name, (neighbor, _) in zone.neighbors.items():
                if n_name not in costs and \
                        neighbor.zone_type != ZoneType.BLOCKED:
                    heapq.heappush(heap, (cost + self.get_cost(zone), n_name))

        return costs
