import sys
from parser import Parser
from simulation import Simulation
from classes import COLORS, Graph


def get_colored(name: str, graph: Graph) -> str:
    zone = graph.get_zone(name)
    color = COLORS.get(zone.color.lower(), "") if zone else ""
    return f"{color}{name}{COLORS['reset']}" if color else name


def print_colored_movements(movements: list[str], graph: Graph) -> None:
    colored_moves = []
    for move in movements:
        parts = move.split('-')
        colored_parts = [parts[0]] + [get_colored(p, graph) for p in parts[1:]]
        colored_moves.append("-".join(colored_parts))
    print(" ".join(colored_moves))


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <map_file>")
        sys.exit(1)

    try:
        graph = Parser.parse_file(sys.argv[1])
        for movements in Simulation(graph).run():
            print_colored_movements(movements, graph)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
