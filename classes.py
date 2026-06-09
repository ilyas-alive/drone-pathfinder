class Graph:
    hub_tags = ['color', 'zone', 'max_drones']
    def __init__(self, nb_drones:int, start_hub, end_hub):
        self.nb_drones = nb_drones
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.zones = [start_hub, end_hub]
        self.connections = []

    def add_hubs(self, hubs):
        for hub in hubs:
            print(hub)
            self.zones.append(Zone(**hub))

    def add_connections(self, connections:list[str]):
        for connection in connections:
            self.connections.append(Connection(**connection))
            

class Zone:
	def __init__(self, name: str,x: int, z: int,
		zone: str = "normal", color: str = "none",max_drones: int = 1) -> None:
		self.name = name
		self.x = x
		self.z = z
		self.zone = zone
		self.color = color
		self.max_drones = max_drones
		self.connections = set()


class Connection:
    def __init__(self, zones:tuple, max_link_capacity:int = 1):
        self.zones = zones
        self.max_link_capacity = max_link_capacity

