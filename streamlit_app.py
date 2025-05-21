import streamlit as st
import pandas as pd
from golf_team_optimizer import Participant, optimize_teams

st.title("Golf Team Optimizer")

uploaded = st.file_uploader("Upload Excel file", type=["xlsx"])
num_teams = st.number_input("Number of teams", min_value=1, step=1, value=2)

if st.button("Start") and uploaded is not None:
    data = pd.read_excel(uploaded, sheet_name=None)

    participants_df = data.get("participants")
    if participants_df is None:
        st.error("Sheet 'participants' not found")
    else:
        ng_df = data.get("ng_pairs")
        decision_df = data.get("decision_pairs")

        participants = [
            Participant(row["name"], int(row["skill"]), bool(row.get("executive", False)))
            for _, row in participants_df.iterrows()
        ]

        ng_pairs = []
        if ng_df is not None:
            for _, row in ng_df.dropna().iterrows():
                ng_pairs.append((row["a"], row["b"]))

        decision_pairs = []
        if decision_df is not None:
            for _, row in decision_df.dropna().iterrows():
                decision_pairs.append((row["a"], row["b"]))

        teams = optimize_teams(
            participants,
            num_teams,
            ng_pairs=ng_pairs or None,
            decision_pairs=decision_pairs or None,
        )

        for i, team in enumerate(teams, 1):
            st.subheader(f"Team {i}")
            for p in team.members:
                st.write(f"{p.name} - Skill {p.skill} - Exec {p.executive}")
            st.write(f"Average skill: {team.skill_average:.2f}")
            st.write(f"Executives: {team.executive_count}")
