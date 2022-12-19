from dataclasses import dataclass
from datetime import datetime
from math import ceil
from multiprocessing import Pool
from queue import PriorityQueue

from util import linenumbers


@dataclass(frozen=True)
class Res:
    ore: int = 0
    clay: int = 0
    obs: int = 0
    geode: int = 0

    def add_res(self, min, robots):
        return Res(
            self.ore + robots.ore * min,
            self.clay + robots.clay * min,
            self.obs + robots.obs * min,
            self.geode + robots.geode * min,
        )

    def add_ore(self):
        return Res(self.ore + 1, self.clay, self.obs, self.geode)

    def add_clay(self):
        return Res(self.ore, self.clay + 1, self.obs, self.geode)

    def add_obs(self):
        return Res(self.ore, self.clay, self.obs + 1, self.geode)

    def add_geode(self):
        return Res(self.ore, self.clay, self.obs, self.geode + 1)

    def build_robot(self, robot):
        return Res(self.ore - robot.ore, self.clay - robot.clay, self.obs - robot.obs, self.geode)

    def __lt__(self, other):
        if self.ore != other.ore:
            return self.ore < other.ore
        if self.clay != other.clay:
            return self.clay < other.ore
        if self.obs != other.obs:
            return self.obs < other.obs
        return self.geode < other.geode


@dataclass
class Blueprint:
    ore: Res
    clay: Res
    obs: Res
    geode: Res


def heuristic(time, robots, res):
    return -((time + 1) * time / 2 + robots.geode * time + res.geode)


def get_max_geodes(blueprint, min):
    q = PriorityQueue()

    q.put((0, min, Res(1, 0, 0, 0), Res(0, 0, 0, 0)))
    while not q.empty():
        u = q.get()
        _, time, robots, res = u

        if time == 0:
            return res.geode

        added_robot = False

        if robots.ore < max(blueprint.ore.ore, blueprint.clay.ore, blueprint.obs.ore, blueprint.geode.ore):
            time_diff = max(ceil((blueprint.ore.ore - res.ore) / robots.ore), 0) + 1
            next_time = time - time_diff
            if next_time >= 0:
                next_robots = robots.add_ore()
                next_res = res.add_res(time_diff, robots).build_robot(blueprint.ore)
                h = heuristic(next_time, next_robots, next_res)
                q.put((h, next_time, next_robots, next_res))
                added_robot = True

        if robots.clay <= (blueprint.obs.clay / blueprint.obs.ore * robots.ore) + 3:
            time_diff = max(ceil((blueprint.clay.ore - res.ore) / robots.ore), 0) + 1
            next_time = time - time_diff
            if next_time >= 0:
                next_robots = robots.add_clay()
                next_res = res.add_res(time_diff, robots).build_robot(blueprint.clay)
                h = heuristic(next_time, next_robots, next_res)
                q.put((h, next_time, next_robots, next_res))
                added_robot = True

        if robots.clay > 0 and robots.obs < (blueprint.geode.obs / blueprint.geode.ore * robots.ore) + 3:
            time_diff = (
                max(
                    ceil((blueprint.obs.ore - res.ore) / robots.ore),
                    ceil((blueprint.obs.clay - res.clay) / robots.clay),
                    0,
                )
                + 1
            )
            next_time = time - time_diff
            if next_time >= 0:
                next_robots = robots.add_obs()
                next_res = res.add_res(time_diff, robots).build_robot(blueprint.obs)
                h = heuristic(next_time, next_robots, next_res)
                q.put((h, next_time, next_robots, next_res))
                added_robot = True

        if robots.obs > 0:
            time_diff = (
                max(
                    ceil((blueprint.geode.ore - res.ore) / robots.ore),
                    ceil((blueprint.geode.obs - res.obs) / robots.obs),
                    0,
                )
                + 1
            )
            next_time = time - time_diff
            if next_time >= 0:
                next_robots = robots.add_geode()
                next_res = res.add_res(time_diff, robots).build_robot(blueprint.geode)
                h = heuristic(next_time, next_robots, next_res)
                q.put((h, next_time, next_robots, next_res))
                added_robot = True

        if not added_robot:
            next_res = res.add_res(time, robots)
            h = heuristic(0, robots, next_res)
            q.put((h, 0, robots, next_res))


def quality(args):
    i, blueprint = args
    geodes = get_max_geodes(blueprint, 24)
    q = geodes * (i + 1)
    return q


if __name__ == "__main__":
    start = datetime.now()
    blueprints = []
    for i, l in linenumbers("in1.txt"):
        ore_ore, rest = l[34:].split(" ore. Each clay robot costs ")
        clay_ore, rest = rest.split(" ore. Each obsidian robot costs ")
        obs_ore, rest = rest.split(" ore and ", maxsplit=1)
        obs_clay, rest = rest.split(" clay. Each geode robot costs ")
        geode_ore, rest = rest.split(" ore and ")
        geode_obs, rest = rest.split(" obsidian.")
        blueprint = Blueprint(
            Res(int(ore_ore)),
            Res(int(clay_ore)),
            Res(int(obs_ore), clay=int(obs_clay)),
            Res(int(geode_ore), obs=int(geode_obs)),
        )
        blueprints.append((i, blueprint))

    with Pool(8) as p:
        print(sum(p.map(quality, blueprints)))
    print(datetime.now() - start)
