# Traffic Route Optimizer (A* Search)

Imagine you are trying to get from Bittan to Bypass and there are a few different roads you could take. Some are shorter, some are longer, and some are just slower because of “traffic vibes”. This project is a small simulation of that situation.

It implements a **Traffic Route Optimizer** using the **A\*** (A-star) search algorithm on a tiny, Bhopal-inspired road network. The idea is to show how an intelligent agent can think about routes, estimate costs, and pick a sensible path instead of guessing.

This is built as a **Bring Your Own Project (BYOP)** for an AI/ML course, so the focus is on clarity, concepts, and reflection—not on building a full Google Maps clone.

---

## 1. What this project actually does

In simple terms, the project:

- Treats a few locations (like `Bittan`, `Jinsi`, `Mall`, `Karond`, `Bypass`) as **nodes** in a small city.
- Treats the roads between them as **edges** with travel times (like 4.5 minutes).
- Uses the **A\*** algorithm to find a route from a start location to a goal location that has the **lowest total cost**.
- Shows two versions of the idea:
  - A more “textbook” A\* with a priority queue (`a_star_route`).
  - A simpler, more intuitive version that still behaves like an informed search (`find_quickest_route`).

If you just want to see it working, you can clone the repo, run one command, and watch it print the best route and total time.

## 2. What you need

Just Python.

- Python **3.8 or newer** is recommended.
- No extra libraries, no installs, no environment drama.

Check your version:

```bash
python --version
 or
python3 --version
```

If you see a Python 3.x version, you’re good.

---

## 3. How to run it (step by step)

### Step 1: Get the code

Clone the repo:

```bash
git clone https://github.com/your-username/traffic-route-optimizer.git
cd traffic-route-optimizer
```

### Step 2: Run the script

```bash
python main.py
# or
python3 main.py
```

You should see something like:

```text
Route: Bittan -> Jinsi -> Mall -> Bypass
Time: 14.8 min

Our Route: Bittan -> Jinsi -> Mall -> Bypass
Time Taken: 14.8 minutes
```

- The first route is from the “proper” A\* implementation: `a_star_route("Bittan", "Bypass")`.
- The second route is from the simple A*-style version: `find_quickest_route("Bittan", "Bypass")`.

They agree on the best path, which is a nice sanity check.

---

## 5. How the city is represented in code

### 5.1. The road network

The “city” is just a small graph:

```python
ROAD_NETWORK = {
    "Bittan": {"Jinsi": 4.5, "Karond": 7.4},
    "Jinsi": {"Bittan": 4.5, "Mall": 6.2},
    "Karond": {"Bittan": 7.4, "Bypass": 9.8},
    "Mall": {"Jinsi": 6.2, "Bypass": 4.1},
    "Bypass": {"Karond": 9.8, "Mall": 4.1},
}
```

You can read this as:

- From **Bittan**:
  - To **Jinsi** takes 4.5 units of time.
  - To **Karond** takes 7.4 units of time.
- And so on for every other location.

There is also a `city_map` in the file that uses the same structure for the simpler function.

### 5.2. The heuristic “sense of direction”

To make A\* efficient, the agent needs a rough sense of how far it is from the goal. This project does that with simple ranks:

```python
HEURISTIC_RANK = {
    "Bittan": 0,
    "Jinsi": 2,
    "Karond": 4,
    "Mall": 5,
    "Bypass": 7,
}
```

The function:

```python
def estimate_remaining_cost(current: str, goal: str) -> float:
    current_h = HEURISTIC_RANK.get(current, 0.0)
    goal_h = HEURISTIC_RANK.get(goal, 0.0)
    return max(0.0, goal_h - current_h)
```

gives the algorithm a **non-negative guess** of how much work is left. It is not perfect, but it is good enough to show how informed search works.

---

## 6. The main brains: A\* and the simpler version

### 6.1. A* (`a_star_route`)

The “real” A\* function does this:

1. Start at the given node.
2. Use a **priority queue** to always pick the most promising node next.
3. Track:
   - `g(n)`: cost so far.
   - `h(n)`: heuristic estimate to the goal.
   - `f(n) = g(n) + h(n)`: total score.
4. Stop once the goal is taken off the queue, and reconstruct the path.

This is the same pattern you see in standard AI textbooks and tutorials.

### 6.2. Simple A*-style (`find_quickest_route`)

The second function is intentionally more “naive”:

- It stores whole paths in a list.
- For each step, it picks the path whose last node has the smallest `g + h`.
- It is slower in theory, but much easier to read and reason about.

This makes it a good teaching tool if you want to explain the idea of “use cost so far plus a guess of what remains” without diving straight into priority queues.

---

## 7. Trying your own map

You can turn this from “Bittan → Bypass” into your own mini-city.

1. Change the graph:

   ```python
   ROAD_NETWORK = {
       "VIT": {"Square": 2.0, "Hostel": 1.5},
       "Square": {"VIT": 2.0, "Market": 3.0},
       "Hostel": {"VIT": 1.5, "Market": 2.5},
       "Market": {"Square": 3.0, "Hostel": 2.5},
   }
   ```

   And update `city_map` similarly.

2. Adjust the heuristic ranks:

   ```python
   HEURISTIC_RANK = {
       "VIT": 0,
       "Hostel": 1,
       "Square": 2,
       "Market": 4,
   }
   ```

3. Change the demo calls:

   ```python
   if __name__ == "__main__":
       route, time = a_star_route("VIT", "Market")
       ...
       best_route, total_time = find_quickest_route("VIT", "Market")
   ```

4. Run `python main.py` again and see the new route.

---

## 8. Why this works well as a BYOP project

This small project quietly covers a lot of AI basics:

- **Intelligent agent**: The code is an agent that chooses a sequence of actions (roads) to reach a goal efficiently.
- **Environment**: The road network is the environment, with states and actions.
- **Problem-solving agent**: The route selection is a classic state-space search problem.
- **Informed search**: A\* shows how adding a heuristic makes search smarter and faster.
- **Rationality**: Given the costs and heuristic, the agent’s choice of route is rational—it minimizes expected cost.

The full reflection, design decisions, limitations, and ideas for future work are written up in `traffic_route_optimizer_report.md`, which pairs with this README for your course submission.

---

## 9. Ideas for future you

If you want to push this further later:

- Compare **A\*** with:
  - Breadth-First Search (BFS)
  - Uniform-Cost Search (Dijkstra)
- Visualize the graph and route using a small GUI or a simple plot.
- Use more realistic heuristics (like distances from rough coordinates).
- Allow users to type start and goal nodes at runtime instead of editing code.

For now, the project stays intentionally small and focused, so that anyone can clone it, read it, and actually understand what is going on.
