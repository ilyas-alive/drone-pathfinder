from __future__ import annotations
from enum import Enum

class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"

class Zone:
    def __init__(self, name: str, x: int, y: int, zone_type: str = "normal", color: str = "none", max_drones: int = 1) -> None:
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.zone_type: ZoneType = ZoneType(zone_type)
        self.color: str = color
        self.max_drones: int = max_drones
        self.connections: list[Connection] = []
        self.neighbors: dict[str, tuple[Zone, Connection]] = {}
        self.is_start: bool = False
        self.is_end: bool = False

    def update_neighbors(self, neighbor: Zone, connection: Connection) -> None:
        if neighbor.name not in self.neighbors:
            self.neighbors[neighbor.name] = (neighbor, connection)
        else:
            raise ValueError("Two connections with the same zones")

    def update_connection(self, connection: Connection) -> None:
        self.connections.append(connection)
        for zone in connection.zones:
            if zone.name != self.name:
                self.update_neighbors(zone, connection)

class Connection:
    def __init__(self, zones: tuple[Zone, Zone], max_link_capacity: int = 1) -> None:
        self.zones: tuple[Zone, Zone] = zones
        self.max_link_capacity: int = max_link_capacity

class Drone:
    def __init__(self, drone_id: int, position: Zone) -> None:
        self.id: int = drone_id
        self.position: Zone = position
        self.state: str = "waiting"
        self.transit_destination: Zone | None = None

    def is_delivered(self) -> bool:
        return self.state == "delivered"

class Graph:
    def __init__(self, nb_drones: int) -> None:
        self.nb_drones: int = nb_drones
        self.start_hub: Zone | None = None
        self.end_hub: Zone | None = None
        self.zones: list[Zone] = []
        self.connections: list[Connection] = []
        self.drones: list[Drone] = []

    def finalize(self) -> None:
        if not self.start_hub or not self.end_hub:
            raise ValueError("Missing start_hub or end_hub")
        self.start_hub.max_drones = 999999
        self.end_hub.max_drones = 999999
        self.start_hub.is_start = True
        self.end_hub.is_end = True
        for i in range(self.nb_drones):
            self.drones.append(Drone(i + 1, self.start_hub))

    def add_zone(self, zone: Zone) -> None:
        self.zones.append(zone)

    def add_connection(self, connection: Connection) -> None:
        self.connections.append(connection)
        for zone in connection.zones:
            zone.update_connection(connection)

    def get_zone(self, name: str) -> Zone | None:
        for zone in self.zones:
            if zone.name == name:
                return zone
        return None
