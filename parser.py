from classes import Graph, Zone

class Parser():
    @staticmethod
    def parse_file(file_name):
        with open(file_name, 'r') as f:
            lines = f.read()

        content = ''
        data_header = ['nb_drones', 'start_hub', 'end_hub', 'hub', 'connection']
        data = {'hubs':[], 'connections':[]}
        header_counter = 0

        for line in lines.split('\n'):
            if line.startswith('# ') or not line:
                continue
            if not line.startswith(tuple(data_header)):
                raise ValueError("ERROR data_header")

            if line.startswith('nb_drones'):
                data['nb_drones'] = int(line.split(':')[1])

            if line.startswith('start_hub'):
                data['start_hub'] = line
            if line.startswith('end_hub'):
                data['end_hub'] = line

            if line.startswith('hub'):
                data['hubs'].append(line)
            if line.startswith('connection'):
                data['connections'].append(line)

        return data


    @staticmethod
    def build_graph(data):
        hub_lines = data['hubs']
        connection_lines = data['connections']
        start_line = Parser.parse_hub(data['start_hub'])
        end_line = Parser.parse_hub(data['end_hub'])

        start_hub = Zone(**start_line)
        end_hub = Zone(**end_line)
        graph = Graph(data['nb_drones'], start_hub, end_hub)

        graph.add_hubs([Parser.parse_hub(l) for l in hub_lines])
        graph.add_connections([Parser.parse_connection(l, graph.zones) for l in connection_lines])
        return graph

    
    @staticmethod
    def parse_hub(line):
        hub_tags = ['max_drones', 'color', 'zone']
        hub = {}
        data = line.split(': ')[1:][0]
        hub['name'] = data.split(' ')[0]
        hub['x'] = data.split(' ')[1]
        hub['z'] = data.split(' ')[2]

        attr_str = data.split('[', 1)[1]
        attr_str = attr_str.split(']', 1)[0] 

        attr = dict(
            attr.split('=')
            for attr in attr_str.split()
            if attr.split('=')[0] in hub_tags
        )
        hub.update(attr)
        return hub

    @staticmethod
    def parse_connection(line, zones):
        try:
            connection = line.split(': ')[1].split('[')[0]
            zone_a, zone_b = connection.split('-')
            zone_a = zone_a.strip()
            zone_b = zone_b.strip()

            max_link_capacity = 1
            if 'max_link_capacity=' in line:
                data = line.split('[')[1].split(']')[0]
                max_link_capacity = int(data.split('=')[1])

        except Exception:
            raise ValueError("Not a valid connection")

        if zone_a not in [zone.name for zone in zones]:
            raise ValueError(f"No Zone with the name {zone_a}")
        if zone_b not in [zone.name for zone in zones]:
            raise ValueError(f"No Zone with the name {zone_b}")

        zones_peer = []
        for name in [zone_a, zone_b]:
            zones_peer.append([zone for zone in zones if zone.name == name][0])
            

        return {
                'zones':tuple(zones_peer),
                'max_link_capacity': max_link_capacity
        }


