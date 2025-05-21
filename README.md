# Golf Teams Optimizer

This repository contains a minimal optimizer for forming golf competition teams.
Participants can be assigned into a number of teams while respecting two types of
pair constraints:

* **NG pairs** – participants that must *not* be on the same team.
* **Decision pairs** – participants that must be on the same team.

The `golf_team_optimizer` module provides a simple heuristic implementation
written in pure Python so it can run without extra dependencies.

## Usage

```python
from golf_team_optimizer import Participant, optimize_teams

members = [
    Participant("Alice", 1, True),
    Participant("Bob", 3, False),
    Participant("Carol", 2, False),
    Participant("Dave", 4, True),
]

teams = optimize_teams(
    members,
    num_teams=2,
    ng_pairs=[("Alice", "Bob")],
    decision_pairs=[("Carol", "Dave")],
)
```

See `tests/test_optimizer.py` for a minimal example.
