class Graph:
    def __init__(self, nb_drones:int, start_hub, end_hub):
        self.nb_drones = nb_drones
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.zones = [start_hub, end_hub]
        self.connections = []

    def add_hubs(self, hubs):
        for hub in hubs:
            self.zones.append(Zone(**hub))

    def add_connections(self, connections:list[str]):
        for connection_data in connections:
            connection = Connection(**connection_data)
            for zone in connection.zones:
                zone.update_connection(connection)


class Zone:
    def __init__(self, name: str,x: int, z: int,
        zone: str = "normal", color: str = "none",max_drones: int = 1) -> None:
        self.name = name
        self.x = x
        self.z = z
        self.zone = zone
        self.color = color
        self.max_drones = max_drones
        self.connections = []
        self.neighbors = {}

    def update_neighbors(self, neighbor, connection):
        if neighbor.name not in self.neighbors:
            self.neighbors.update(neighbor.name: (zone, connection)})
        else:
            raise ValueError("Two connections with the same zones")

    def update_connection(self, connection):
        self.connections.append(connection)
        for zones in connection.zones:
            if zone.name != self.name:
                self.update_neighbors(zone, connection)

class Connection:
    def __init__(self, zones:tuple, max_link_capacity:int = 1):
        self.zones = zones
        self.max_link_capacity = max_link_capacity

