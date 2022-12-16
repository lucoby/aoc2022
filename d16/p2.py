from dataclasses import dataclass
from queue import PriorityQueue
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


def heuristic(valves, opened, time):
    flow = sum([valve.flow_rate for v, valve in valves.items() if v not in opened])
    return flow * time


def best_path(valves, time):
    q = PriorityQueue()
    q.put((0, time, frozenset({"AA"}), "AA", 0))

    explored = {}

    while not q.empty():
        u = q.get()
        _, time, opened, current, total_pressure = u

        explored[opened] = max(total_pressure, explored.get(opened, 0))

        if time == 0 or len(opened) == len(valves):
            return explored

        for v, valve in valves.items():
            if v not in opened:
                distance = valves[current].distance[v] + 1
                if distance <= time:
                    time_left = time - distance
                    pressure = time_left * valve.flow_rate + total_pressure
                    new_opened = opened | {v}
                else:
                    new_opened = opened
                    pressure = total_pressure
                    time_left = 0

                h = heuristic(valves, new_opened, time_left) + pressure

                n = (-h, time_left, new_opened, v, pressure)
                q.put(n)


if __name__ == "__main__":
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

    explored = best_path(valves, 26)

    max_pressure = 0
    for h, h_p in explored.items():
        for e, e_p in explored.items():
            both = h & e
            if len(both) == 1:
                max_pressure = max(max_pressure, h_p + e_p)

    print(max_pressure)
