from collections import defaultdict
from classes import Graph, ZoneType, Connection
from pathfinder import PathFinder


class Simulation:
    def __init__(self, graph: Graph) -> None:
        self.graph: Graph = graph
        self.costs: dict[str, float] = PathFinder(self.graph).compute_costs()

    def run_turn(self) -> list[str]:
        movements: list[str] = []
        moved_this_turn: set[int] = set()

        zone_occupants: dict[str, int] = defaultdict(int)
        connection_usage: dict[Connection, int] = defaultdict(int)

        for d in self.graph.drones:
            if not d.is_delivered():
                if d.state == "in_transit":
                    target = d.transit_destination.name
                else:
                    target = d.position.name
                zone_occupants[target] += 1

        for d in self.graph.drones:
            if d.state == "in_transit" and d.transit_destination:
                dest = d.transit_destination
                connection_usage[d.position.neighbors[dest.name][1]] += 1
                d.position, d.transit_destination = dest, None
                d.state = "delivered" if dest.is_end else "waiting"

                movements.append(f"D{d.id}-{dest.name}")
                moved_this_turn.add(d.id)

        drones = sorted(
            self.graph.drones,
            key=lambda x: self.costs.get(x.position.name, float('inf'))
        )
        for d in drones:
            if d.is_delivered() or d.id in moved_this_turn:
                continue
            if d.position.is_start:
                best_cost = float('inf')
            else:
                best_cost = self.costs[d.position.name]
            best_neighbor, best_load = None, float('inf')

            for n_name, (neighbor, conn) in d.position.neighbors.items():
                if neighbor.zone_type == ZoneType.BLOCKED or \
                        n_name not in self.costs:
                    continue
                if not neighbor.is_end and not neighbor.is_start and \
                        zone_occupants[n_name] >= neighbor.max_drones:
                    continue
                if connection_usage[conn] >= conn.max_link_capacity:
                    continue

                cost, load = self.costs[n_name], zone_occupants[n_name]
                if cost < best_cost or \
                        (cost == best_cost and load < best_load):
                    best_cost, best_neighbor, best_load = cost, neighbor, load

            if not best_neighbor:
                continue

            connection_usage[d.position.neighbors[best_neighbor.name][1]] += 1
            zone_occupants[d.position.name] -= 1
            zone_occupants[best_neighbor.name] += 1

            if best_neighbor.zone_type == ZoneType.RESTRICTED:
                d.state, d.transit_destination = "in_transit", best_neighbor
                movements.append(
                    f"D{d.id}-{d.position.name}-{best_neighbor.name}"
                )
            else:
                d.position = best_neighbor
                d.state = "delivered" if best_neighbor.is_end else "waiting"
                movements.append(f"D{d.id}-{best_neighbor.name}")

            moved_this_turn.add(d.id)

        movements.sort(key=lambda x: int(x.split('-')[0][1:]))
        return movements

    def run(self) -> list[list[str]]:
        history: list[list[str]] = []
        if not self.graph.start_hub or \
                self.graph.start_hub.name not in self.costs:
            raise ValueError("Invalid start_hub or no path to goal")

        while not all(d.is_delivered() for d in self.graph.drones):
            movements = self.run_turn()
            if movements:
                history.append(movements)
            elif (
                any(d.state != "delivered" for d in self.graph.drones)
                and not any(d.state == "in_transit" for d in self.graph.drones)
            ):
                raise ValueError("Simulation deadlocked!")
            else:
                break
        return history
