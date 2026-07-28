from classes import Graph, Zone, Connection

class Parser:
    @staticmethod
    def _split_meta(line):
        if '[' in line:
            idx = line.index('[')
            return line[:idx].strip(), line[idx+1:-1].strip()
        return line.strip(), ""

    @staticmethod
    def parse_file(file_name):
        with open(file_name, 'r') as f:
            lines = [line.split('#')[0].strip() for line in f if line.split('#')[0].strip()]

        graph = Graph(int(lines[0].split(':')[1]))

        for line in lines[1:]:
            if line.startswith(('start_hub:', 'end_hub:', 'hub:')):
                prefix = line.split(':')[0]
                zone = Parser.parse_hub(line[len(prefix)+1:].strip())
                graph.add_zone(zone)
                
                if prefix == 'start_hub':
                    graph.start_hub = zone
                elif prefix == 'end_hub':
                    graph.end_hub = zone

            elif line.startswith('connection:'):
                conn = Parser.parse_connection(line[11:].strip(), graph)
                graph.add_connection(conn)

        graph.finalize()
        return graph

    @staticmethod
    def parse_hub(line):
        data_part, meta_part = Parser._split_meta(line)
        parts = data_part.split()
        z_args = {"name": parts[0], "x": int(parts[1]), "y": int(parts[2])}
        for token in meta_part.split():
            key, val = token.split('=', 1)
            if key == 'max_drones': z_args['max_drones'] = int(val)
            elif key == 'zone': z_args['zone_type'] = val
            else: z_args[key] = val
        return Zone(**z_args)

    @staticmethod
    def parse_connection(line, graph):
        conn_part, meta_part = Parser._split_meta(line)
        za_name, zb_name = [x.strip() for x in conn_part.split('-', 1)]
        za, zb = graph.get_zone(za_name), graph.get_zone(zb_name)

        cap = 1
        for token in meta_part.split():
            key, val = token.split('=', 1)
            if key == 'max_link_capacity': cap = int(val)

        return Connection((za, zb), cap)
