# Golf Teams Optimizer

This repository contains a minimal optimizer for forming golf competition teams.
Participants can be assigned into a number of teams while respecting two types of
pair constraints:

* **NG pairs** – participants that must *not* be on the same team.
* **Decision pairs** – participants that must be on the same team.

The `golf_team_optimizer` module provides a simple heuristic implementation
written in pure Python so it can run without extra dependencies.

## Setup

Install the Python dependencies listed in `requirements.txt` before running the
code. If you are using Codex you can simply execute the provided setup script:

```bash
./setup.sh
```

This installs packages such as `openpyxl`, `pandas`, `streamlit` and `pytest` so
the application and tests can run offline.

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

## Streamlit UI

A simple Streamlit application is provided in `streamlit_app.py` for interactive use. The expected Excel file should contain three sheets:

1. `participants` – columns `name`, `skill`, and optional `executive`.
2. `ng_pairs` – optional, columns `a` and `b` listing pairs that must **not** be on the same team.
3. `decision_pairs` – optional, columns `a` and `b` listing pairs that must be on the same team.

Run the app locally with:

```bash
streamlit run streamlit_app.py
```

Upload the Excel file and press **Start** to see the generated teams.
