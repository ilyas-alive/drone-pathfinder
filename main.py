import sys
from parser import Parser
from simulation import Simulation

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <map_file>")
        sys.exit(1)

    try:
        graph = Parser.parse_file(sys.argv[1])
        for movements in Simulation(graph).run():
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
