from golf_team_optimizer import Participant, optimize_teams


def test_pairs_respected():
    participants = [
        Participant('A', 1),
        Participant('B', 2),
        Participant('C', 3),
        Participant('D', 4),
    ]
    teams = optimize_teams(
        participants,
        num_teams=2,
        ng_pairs=[('A', 'B')],
        decision_pairs=[('C', 'D')],
    )
    # Check C and D are together
    team_with_c = next(t for t in teams if any(p.name == 'C' for p in t.members))
    assert any(p.name == 'D' for p in team_with_c.members)
    # Check A and B are not on same team
    team_a = next(t for t in teams if any(p.name == 'A' for p in t.members))
    team_b = next(t for t in teams if any(p.name == 'B' for p in t.members))
    assert team_a is not team_b
