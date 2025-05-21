from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Set

@dataclass
class Participant:
    """Represents a single participant."""
    name: str
    skill: int
    executive: bool = False

    def __hash__(self) -> int:  # allow using in sets
        return hash(self.name)

@dataclass
class Team:
    """Represents a team of participants."""
    members: List[Participant] = field(default_factory=list)

    def add(self, participant: Participant) -> None:
        self.members.append(participant)

    @property
    def skill_average(self) -> float:
        if not self.members:
            return 0.0
        return sum(p.skill for p in self.members) / len(self.members)

    @property
    def executive_count(self) -> int:
        return sum(1 for p in self.members if p.executive)

    def has(self, participant: Participant) -> bool:
        return participant in self.members

    def conflicts_with(self, participant: Participant, ng_map: Dict[str, Set[str]]) -> bool:
        """Check if adding the participant conflicts with existing members."""
        for p in self.members:
            if participant.name in ng_map.get(p.name, set()):
                return True
        return False


def build_clusters(participants: List[Participant], decision_pairs: List[Tuple[str, str]]) -> List[Set[Participant]]:
    """Build clusters of participants that must be on the same team."""
    parent: Dict[str, str] = {}
    def find(x: str) -> str:
        parent.setdefault(x, x)
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    def union(a: str, b: str) -> None:
        pa, pb = find(a), find(b)
        if pa != pb:
            parent[pb] = pa

    for a, b in decision_pairs:
        union(a, b)

    clusters: Dict[str, Set[Participant]] = {}
    lookup = {p.name: p for p in participants}
    for p in participants:
        key = find(p.name)
        clusters.setdefault(key, set()).add(p)
    return list(clusters.values())


def optimize_teams(
    participants: List[Participant],
    num_teams: int,
    ng_pairs: List[Tuple[str, str]] | None = None,
    decision_pairs: List[Tuple[str, str]] | None = None,
) -> List[Team]:
    """Simple heuristic optimizer for forming teams with pair constraints."""
    if num_teams <= 0:
        raise ValueError("num_teams must be positive")

    ng_map: Dict[str, Set[str]] = {}
    if ng_pairs:
        for a, b in ng_pairs:
            ng_map.setdefault(a, set()).add(b)
            ng_map.setdefault(b, set()).add(a)

    decision_pairs = decision_pairs or []
    clusters = build_clusters(participants, decision_pairs)

    teams = [Team() for _ in range(num_teams)]

    # sort clusters by average skill descending
    clusters.sort(key=lambda c: sum(p.skill for p in c) / len(c), reverse=True)

    for cluster in clusters:
        # find candidate teams that do not violate NG constraints
        candidate_scores = []
        for team in teams:
            if any(team.conflicts_with(p, ng_map) for p in cluster):
                continue
            # compute projected average skill if cluster added
            projected = team.members + list(cluster)
            avg = sum(p.skill for p in projected) / len(projected)
            candidate_scores.append((abs(avg), len(team.members), team))
        if not candidate_scores:
            raise ValueError("No feasible team assignment for cluster" + str([p.name for p in cluster]))
        # choose team with fewest members then lowest average skill
        candidate_scores.sort(key=lambda x: (x[1], x[0]))
        selected_team = candidate_scores[0][2]
        for p in cluster:
            selected_team.add(p)

    return teams
