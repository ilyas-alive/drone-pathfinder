from __future__ import annotations
from enum import Enum

class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"

class Zone:
    def __init__(self, name, x, y, zone_type="normal", color="none", max_drones=1):
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = ZoneType(zone_type)
        self.color = color
        self.max_drones = max_drones
        self.connections = []
        self.neighbors = {}
        self.is_start = False
        self.is_end = False

    def update_neighbors(self, neighbor, connection):
        self.neighbors[neighbor.name] = (neighbor, connection)

    def update_connection(self, connection):
        self.connections.append(connection)
        for zone in connection.zones:
            if zone.name != self.name:
                self.update_neighbors(zone, connection)

class Connection:
    def __init__(self, zones, max_link_capacity=1):
        self.zones = zones
        self.max_link_capacity = max_link_capacity

class Drone:
    def __init__(self, drone_id, position):
        self.id = drone_id
        self.position = position
        self.state = "waiting"
        self.transit_destination = None

    def is_delivered(self):
        return self.state == "delivered"

class Graph:
    def __init__(self, nb_drones):
        self.nb_drones = nb_drones
        self.start_hub = None
        self.end_hub = None
        self.zones = []
        self.connections = []
        self.drones = []

    def finalize(self):
        self.start_hub.max_drones = 999999
        self.end_hub.max_drones = 999999
        self.start_hub.is_start = True
        self.end_hub.is_end = True
        for i in range(self.nb_drones):
            self.drones.append(Drone(i + 1, self.start_hub))

    def add_zone(self, zone):
        self.zones.append(zone)

    def add_connection(self, connection):
        self.connections.append(connection)
        for zone in connection.zones:
            zone.update_connection(connection)

    def get_zone(self, name):
        for zone in self.zones:
            if zone.name == name:
                return zone
        return None
