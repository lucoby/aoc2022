from dataclasses import dataclass
from functools import lru_cache

from util import linenumbers


@dataclass
class Res:
    ore: int = 0
    clay: int = 0
    obs: int = 0
    geode: int = 0

    def __hash__(self):
        return hash((self.ore, self.clay, self.obs, self.geode))


@dataclass
class Blueprint:
    ore: Res
    clay: Res
    obs: Res
    geode: Res

    def __hash__(self):
        return hash((self.ore.__hash__(), self.clay.__hash__(), self.obs.__hash__(), self.geode.__hash__()))


@lru_cache(maxsize=None)
def get_max_geodes(blueprint, min, robots, res):
    if min == 24:
        return res.geode + robots.geode

    if robots.ore > max(blueprint.ore.ore, blueprint.clay.ore, blueprint.obs.ore, blueprint.geode.ore) or robots.clay > (blueprint.obs.clay / blueprint.obs.ore * robots.ore) + 2 or robots.obs > (blueprint.geode.obs / blueprint.geode.ore * robots.ore) + 2:
        return 0

    if blueprint.geode.ore <= res.ore and blueprint.geode.obs <= res.obs:
        return get_max_geodes(
            blueprint,
            min + 1,
            Res(ore=robots.ore , clay=robots.clay, obs=robots.obs, geode=robots.geode + 1),
            Res(
                ore=res.ore + robots.ore - blueprint.geode.ore,
                clay=res.clay + robots.clay,
                obs=res.obs + robots.obs - blueprint.geode.obs,
                geode=res.geode + robots.geode,
            ),
        )

    max_geodes = []
    if blueprint.ore.ore <= res.ore:
        max_geodes.append(
            get_max_geodes(
                blueprint,
                min + 1,
                Res(ore=robots.ore + 1, clay=robots.clay, obs=robots.obs, geode=robots.geode),
                Res(
                    ore=res.ore + robots.ore - blueprint.ore.ore,
                    clay=res.clay + robots.clay,
                    obs=res.obs + robots.obs,
                    geode=res.geode + robots.geode,
                ),
            ),
        )
    if blueprint.clay.ore <= res.ore:
        max_geodes.append(
            get_max_geodes(
                blueprint,
                min + 1,
                Res(ore=robots.ore, clay=robots.clay + 1, obs=robots.obs, geode=robots.geode),
                Res(
                    ore=res.ore + robots.ore - blueprint.clay.ore,
                    clay=res.clay + robots.clay,
                    obs=res.obs + robots.obs,
                    geode=res.geode + robots.geode,
                ),
            ),
        )
    if blueprint.obs.ore <= res.ore and blueprint.obs.clay <= res.clay:
        max_geodes.append(
            get_max_geodes(
                blueprint,
                min + 1,
                Res(ore=robots.ore , clay=robots.clay, obs=robots.obs + 1, geode=robots.geode),
                Res(
                    ore=res.ore + robots.ore - blueprint.obs.ore,
                    clay=res.clay + robots.clay - blueprint.obs.clay,
                    obs=res.obs + robots.obs,
                    geode=res.geode + robots.geode,
                ),
            ),
        )

    max_geodes.append(get_max_geodes(
            blueprint,
            min + 1,
            robots,
            Res(
                ore=res.ore + robots.ore,
                clay=res.clay + robots.clay,
                obs=res.obs + robots.obs,
                geode=res.geode + robots.geode,
            ),
        ))
    return max(max_geodes)

if __name__ == "__main__":
    all_q = 0
    for i, l in linenumbers("in1.txt"):
        ore_ore, rest = l[34:].split(" ore. Each clay robot costs ")
        clay_ore, rest = rest.split(" ore. Each obsidian robot costs ")
        obs_ore, rest = rest.split(" ore and ", maxsplit=1)
        obs_clay, rest = rest.split(" clay. Each geode robot costs ")
        geode_ore, rest = rest.split(" ore and ")
        geode_obs, rest = rest.split(" obsidian.")
        blueprint = Blueprint(
            ore=Res(ore=int(ore_ore)),
            clay=Res(ore=int(clay_ore)),
            obs=Res(ore=int(obs_ore), clay=int(obs_clay)),
            geode=Res(ore=int(geode_ore), obs=int(geode_obs)),
        )
        print(blueprint)
        geodes = get_max_geodes(blueprint, 1, Res(ore=1), Res())
        quality = geodes * (i + 1)
        print(geodes)
        all_q += quality
    print(all_q)
