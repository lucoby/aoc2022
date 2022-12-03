import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import pytz


@dataclass
class Finish:
    name: str
    time: timedelta


if __name__ == '__main__':
    year = 2022
    reformatted = {}
    for i in range(25):
        reformatted[str(i + 1)] = {"1": [], "2": []}
    with open("res.json") as f:
        res = json.load(f)
        for _id, user in res["members"].items():
            for day_i, day in user["completion_day_level"].items():
                for part_i, part in day.items():
                    finish = Finish(
                        name=user["name"],
                        time=datetime.utcfromtimestamp(
                            part["get_star_ts"]).replace(tzinfo=timezone.utc) - datetime(year=year, month=12, day=int(day_i), tzinfo=pytz.timezone("US/Eastern"))
                    )
                    reformatted[day_i][part_i].append(finish)

    for i in range(25):
        for j in range(2):
            if len(reformatted[str(i + 1)][str(j + 1)]) > 0:
                print()
                print(f"Day {i + 1} Part {j + 1}")
                reformatted[str(i + 1)][str(j + 1)].sort(key=lambda x: x.time)
                for f in reformatted[str(i + 1)][str(j + 1)]:
                    print(f"{f.name: <20} {f.time}")
