from collections import defaultdict
from classes import Graph, ZoneType
from pathfinder import PathFinder

class Simulation:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.costs = PathFinder(self.graph).compute_costs()

    def run_turn(self):
        movements = []
        moved_this_turn = set()
        zone_occupants = defaultdict(int)
        connection_usage = defaultdict(int)

        for d in self.graph.drones:
            if not d.is_delivered():
                zone_occupants[d.position.name] += 1

        for d in self.graph.drones:
            if d.state == "in_transit" and d.transit_destination:
                dest = d.transit_destination
                d.position, d.transit_destination = dest, None
                d.state = "delivered" if dest.is_end else "waiting"
                movements.append(f"D{d.id}-{dest.name}")
                moved_this_turn.add(d.id)

        for d in self.graph.drones:
            if d.is_delivered() or d.id in moved_this_turn:
                continue

            best_cost = self.costs.get(d.position.name, float('inf'))
            best_neighbor = None

            for n_name, (neighbor, conn) in d.position.neighbors.items():
                if neighbor.zone_type == ZoneType.BLOCKED or n_name not in self.costs:
                    continue
                if not neighbor.is_end and zone_occupants[n_name] >= neighbor.max_drones:
                    continue
                if connection_usage[conn] >= conn.max_link_capacity:
                    continue

                cost = self.costs[n_name]
                if cost < best_cost:
                    best_cost = cost
                    best_neighbor = neighbor

            if not best_neighbor:
                continue

            connection_usage[d.position.neighbors[best_neighbor.name][1]] += 1
            zone_occupants[d.position.name] -= 1
            zone_occupants[best_neighbor.name] += 1

            if best_neighbor.zone_type == ZoneType.RESTRICTED:
                d.state, d.transit_destination = "in_transit", best_neighbor
                movements.append(f"D{d.id}-{d.position.name}-{best_neighbor.name}")
            else:
                d.position = best_neighbor
                d.state = "delivered" if best_neighbor.is_end else "waiting"
                movements.append(f"D{d.id}-{best_neighbor.name}")

            moved_this_turn.add(d.id)

        return movements

    def run(self):
        history = []
        while not all(d.is_delivered() for d in self.graph.drones):
            movements = self.run_turn()
            if movements:
                history.append(movements)
            else:
                break
        return history
