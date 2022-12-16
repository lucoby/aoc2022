from dataclasses import dataclass
from typing import Dict

import networkx as nx

from util import lines

@dataclass
class Valve:
    name: str
    flow_rate: int
    distance: Dict = None

    @staticmethod
    def parse(l):
        name = l[6:8]
        flow_rate = int(l[23:].split(";")[0])
        if len(l.strip().split("tunnels lead to valves ")) > 1:
            tunnels = l.strip().split("tunnels lead to valves ")[1].split(", ")
        else:
            tunnels = l.strip().split("tunnel leads to valve ")[1].split(", ")
        return Valve(name=name, flow_rate=flow_rate), tunnels


def best_path(valves, opened, time1, time2, current1, current2, total_pressure):
    if max(time1, time2) <= 0:
        return total_pressure
    best_pressure = total_pressure

    for v, valve in valves.items():
        if v not in opened:
            if time1 >= time2:
                distance = valves[current1].distance[v] + 1
                pressure = (time1 - distance) * valve.flow_rate + total_pressure
                new_opened = opened.copy()
                new_opened.add(v)

                final_pressure = best_path(valves, new_opened, time1 - distance, time2, v, current2, pressure)
                best_pressure = max(best_pressure, final_pressure)
            else:
                distance = valves[current2].distance[v] + 1
                pressure = (time2 - distance) * valve.flow_rate + total_pressure
                new_opened = opened.copy()
                new_opened.add(v)

                final_pressure = best_path(valves, new_opened, time1, time2 - distance, current1, v, pressure)
                best_pressure = max(best_pressure, final_pressure)
    return best_pressure


if __name__ == '__main__':
    valves = {}
    g = nx.Graph()
    for l in lines("in1.txt"):
        valve, tunnels = Valve.parse(l)
        valves[valve.name] = valve
        g.add_edges_from([(valve.name, t) for t in tunnels])

    shortest_paths = dict(nx.all_pairs_shortest_path(g))

    for s, target_path in shortest_paths.items():
        distance = {t: len(path) - 1 for t, path in target_path.items()}
        valves[s].distance = distance

    valves = {v: valve for v, valve in valves.items() if v == "AA" or valve.flow_rate > 0}

    current = "AA"
    opened = set()
    total_pressure = best_path(valves, opened, 26, 26, current, current, 0)
    print(total_pressure)


    print(valves)
