from __future__ import annotations

from heapq import heappop, heappush
from typing import Dict, List, Optional, Tuple

ROAD_NETWORK: Dict[str, Dict[str, float]] = {
    "Bittan": {"Jinsi": 4.5, "Karond": 7.4},
    "Jinsi": {"Bittan": 4.5, "Mall": 6.2},
    "Karond": {"Bittan": 7.4, "Bypass": 9.8},
    "Mall": {"Jinsi": 6.2, "Bypass": 4.1},
    "Bypass": {"Karond": 9.8, "Mall": 4.1},
}
HEURISTIC_RANK: Dict[str, float] = {
    "Bittan": 0,
    "Jinsi": 2,
    "Karond": 4,
    "Mall": 5,
    "Bypass": 7,
}
def estimate_remaining_cost(current: str, goal: str) -> float:
    """Estimate remaining travel cost from `current` to `goal` (A* heuristic)."""
    current_h = HEURISTIC_RANK.get(current, 0.0)
    goal_h = HEURISTIC_RANK.get(goal, 0.0)

    return max(0.0, goal_h - current_h)

def a_star_route(start: str, goal: str) -> Tuple[Optional[List[str]], float]:

    if start not in ROAD_NETWORK or goal not in ROAD_NETWORK:
        return None, float("inf")

    open_set: List[Tuple[float, float, List[str], str]] = []
    heappush(open_set, (estimate_remaining_cost(start, goal), 0.0, [start], start))

    best_g: Dict[str, float] = {start: 0.0}

    while open_set:
        _, g, path, current = heappop(open_set)

        if current == goal:
            return path, g

        if g != best_g.get(current, float("inf")):
            continue

        for neighbor, step_cost in ROAD_NETWORK[current].items():
            new_g = g + step_cost
            if new_g < best_g.get(neighbor, float("inf")):
                best_g[neighbor] = new_g
                new_path = path + [neighbor]
                f = new_g + estimate_remaining_cost(neighbor, goal)
                heappush(open_set, (f, new_g, new_path, neighbor))

    return None, float("inf")

city_map = {
    "Bittan": {"Jinsi": 4.5, "Karond": 7.4},
    "Jinsi": {"Bittan": 4.5, "Mall": 6.2},
    "Karond": {"Bittan": 7.4, "Bypass": 9.8},
    "Mall": {"Jinsi": 6.2, "Bypass": 4.1},
    "Bypass": {"Karond": 9.8, "Mall": 4.1},
}
def guess_remaining_distance(current_location, destination):
    location_scores = {
        "Bittan": 0,
        "Jinsi": 2,
        "Karond": 4,
        "Mall": 5,
        "Bypass": 7,
    }
    return abs(location_scores[destination] - location_scores[current_location])
def find_quickest_route(start, goal):
    paths_to_explore = [[start]]

    fastest_times = {start: 0}

    while paths_to_explore:
        current_path = min(
            paths_to_explore,
            key=lambda path: fastest_times[path[-1]] + guess_remaining_distance(path[-1], goal),
        )
        paths_to_explore.remove(current_path)

        current_location = current_path[-1]

        if current_location == goal:
            return current_path, fastest_times[current_location]

        for next_stop, travel_time in city_map[current_location].items():
            total_time = fastest_times[current_location] + travel_time

            if next_stop not in fastest_times or total_time < fastest_times[next_stop]:
                fastest_times[next_stop] = total_time
                paths_to_explore.append(current_path + [next_stop])

    return None, 999


if __name__ == "__main__":
    route, time = a_star_route("Bittan", "Bypass")
    if route is None:
        print("No route found.")
    else:
        print("Route:", " -> ".join(route))
        print("Time:", round(time, 1), "min")
  
    best_route, total_time = find_quickest_route("Bittan", "Bypass")

    print("Our Route: ".join(best_route))
    print("Time Taken: ", round(total_time, 1), "minutes")                    fully  EXPLAIN the code
