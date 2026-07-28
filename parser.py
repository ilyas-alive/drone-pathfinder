from classes import Graph, Zone, Connection

class Parser:
    @staticmethod
    def _split_meta(line: str) -> tuple[str, str]:
        if '[' in line:
            if not line.endswith(']'):
                raise ValueError("Unclosed metadata block")
            idx = line.index('[')
            return line[:idx].strip(), line[idx+1:-1].strip()
        return line.strip(), ""

    @staticmethod
    def parse_file(file_name: str) -> Graph:
        with open(file_name, 'r') as f:
            lines = [line.split('#')[0].strip() for line in f if line.split('#')[0].strip()]

        if not lines or not lines[0].startswith('nb_drones:'):
            raise ValueError("First line must be nb_drones")
        
        graph = Graph(int(lines[0].split(':')[1]))
        seen_connections = set()

        for line in lines[1:]:
            if line.startswith(('start_hub:', 'end_hub:', 'hub:')):
                prefix = line.split(':')[0]
                zone = Parser.parse_hub(line[len(prefix)+1:].strip())
                if graph.get_zone(zone.name):
                    raise ValueError(f"Duplicate zone name: {zone.name}")
                graph.add_zone(zone)
                
                if prefix == 'start_hub':
                    graph.start_hub = zone
                elif prefix == 'end_hub':
                    graph.end_hub = zone

            elif line.startswith('connection:'):
                conn = Parser.parse_connection(line[11:].strip(), graph)
                names_t = tuple(sorted([conn.zones[0].name, conn.zones[1].name]))
                if names_t in seen_connections:
                    raise ValueError(f"Duplicate connection: {line}")
                seen_connections.add(names_t)
                graph.add_connection(conn)
            else:
                raise ValueError(f"Unknown instruction: {line}")

        graph.finalize()
        return graph

    @staticmethod
    def parse_hub(line: str) -> Zone:
        data_part, meta_part = Parser._split_meta(line)
        parts = data_part.split()
        if len(parts) != 3 or '-' in parts[0]:
            raise ValueError(f"Invalid hub format: {data_part}")

        z_args = {"name": parts[0], "x": int(parts[1]), "y": int(parts[2])}
        for token in meta_part.split():
            key, val = token.split('=', 1)
            if key == 'max_drones': z_args['max_drones'] = int(val)
            elif key == 'zone': z_args['zone_type'] = val
            else: z_args[key] = val

        return Zone(**z_args)

    @staticmethod
    def parse_connection(line: str, graph: Graph) -> Connection:
        conn_part, meta_part = Parser._split_meta(line)
        if '-' not in conn_part:
            raise ValueError("Connection must contain '-'")

        za_name, zb_name = [x.strip() for x in conn_part.split('-', 1)]
        za, zb = graph.get_zone(za_name), graph.get_zone(zb_name)
        
        if not za or not zb or za.name == zb.name:
            raise ValueError(f"Invalid zones in connection: {conn_part}")

        cap = 1
        for token in meta_part.split():
            key, val = token.split('=', 1)
            if key == 'max_link_capacity': cap = int(val)

        return Connection((za, zb), cap)
