import pandas as pd
import pulp
from load_csvs import get_dataframe_from_csvs


def get_position_df(df, position):
    df_pos = df[df['pos'] == position]
    return df_pos


def get_player_dict(df):
    players = {}
    for index, row in df.iterrows():
        player = {"pos": row['pos'], "name": row['name'], "team": row['team'], "ppg": row['ppg'],
                  "avg_salary": row['avg_salary'], "drafted_starter": pulp.LpVariable(f"{row['name']}_starter", cat="Binary"),
                  "drafted_reserve": pulp.LpVariable(f"{row['name']}_reserve", cat="Binary")}
        players[row['name']] = player
    return players


df = get_dataframe_from_csvs()

# build position dataframes
df_qbs = get_position_df(df, 'QB')
df_rbs = get_position_df(df, 'RB')
df_wrs = get_position_df(df, 'WR')
df_tes = get_position_df(df, 'TE')
df_kickers = get_position_df(df, 'K')
df_dsts = get_position_df(df, 'D/ST')

# Create the pulp solver problem
problem = pulp.LpProblem("CategoryConstraintProblem", pulp.LpMaximize)

# create a dictionary with the player name as the key
qbs = get_player_dict(df_qbs)
rbs = get_player_dict(df_rbs)
wrs = get_player_dict(df_wrs)
tes = get_player_dict(df_tes)
kickers = get_player_dict(df_kickers)
dsts = get_player_dict(df_dsts)

# objective function. Maximize points
problem += pulp.lpSum(
# weight starter points as .8 
    [qbs[qb]["ppg"] * .8 * qbs[qb]["drafted_starter"] for qb in qbs]
) + pulp.lpSum(
    [rbs[rb]["ppg"] * .8 * rbs[rb]["drafted_starter"] for rb in rbs]
) + pulp.lpSum(
    [wrs[wr]["ppg"] * .8 * wrs[wr]["drafted_starter"] for wr in wrs]
) + pulp.lpSum(
    [tes[te]["ppg"] * .8 * tes[te]["drafted_starter"] for te in tes]
) + pulp.lpSum(
    [kickers[kicker]["ppg"] * kickers[kicker]["drafted_starter"] for kicker in kickers]
) + pulp.lpSum(
    [dsts[dst]["ppg"] * dsts[dst]["drafted_starter"] for dst in dsts]
) + pulp.lpSum(
# weight reserve points as .2
    [qbs[qb]["ppg"] * .2 * qbs[qb]["drafted_reserve"] for qb in qbs]
) + pulp.lpSum(
    [rbs[rb]["ppg"] * .2 * rbs[rb]["drafted_reserve"] for rb in rbs]
) + pulp.lpSum(
    [wrs[wr]["ppg"] * .2 * wrs[wr]["drafted_reserve"] for wr in wrs]
) + pulp.lpSum(
    [tes[te]["ppg"] * .2 * tes[te]["drafted_reserve"] for te in tes]
)


# salary constraint
problem += pulp.lpSum(
    [qbs[qb]["avg_salary"] * qbs[qb]["drafted_starter"] for qb in qbs]
) + pulp.lpSum(
    [rbs[rb]["avg_salary"] * rbs[rb]["drafted_starter"] for rb in rbs]
) + pulp.lpSum(
    [wrs[wr]["avg_salary"] * wrs[wr]["drafted_starter"] for wr in wrs]
) + pulp.lpSum(
    [tes[te]["avg_salary"] * tes[te]["drafted_starter"] for te in tes]  
) + pulp.lpSum(
    [kickers[kicker]["avg_salary"] * kickers[kicker]["drafted_starter"] for kicker in kickers]
) + pulp.lpSum(
    [dsts[dst]["avg_salary"] * dsts[dst]["drafted_starter"] for dst in dsts]
) + pulp.lpSum(
    [qbs[qb]["avg_salary"] * qbs[qb]["drafted_reserve"] for qb in qbs]
) + pulp.lpSum(
    [rbs[rb]["avg_salary"] * rbs[rb]["drafted_reserve"] for rb in rbs]
) + pulp.lpSum(
    [wrs[wr]["avg_salary"] * wrs[wr]["drafted_reserve"] for wr in wrs]
) + pulp.lpSum(
    [tes[te]["avg_salary"] * tes[te]["drafted_reserve"] for te in tes]
) <= 200

# only 1 qb starter constraint
problem += pulp.lpSum(
    [qbs[qb]["drafted_starter"] for qb in qbs]
) == 1

# 2 rb starters
problem += pulp.lpSum(
    [rbs[rb]["drafted_starter"] for rb in rbs]
) >= 2

# 2 wr starters
problem += pulp.lpSum(
    [wrs[wr]["drafted_starter"] for wr in wrs]
) >= 2

# 1 te starter
problem += pulp.lpSum(
    [tes[te]["drafted_starter"] for te in tes]
) >= 1

# 1 flex starter
problem += pulp.lpSum(
    [rbs[rb]["drafted_starter"] for rb in rbs]
) + pulp.lpSum(
    [wrs[wr]["drafted_starter"] for wr in wrs]
) + pulp.lpSum(
    [tes[te]["drafted_starter"] for te in tes]
) == 6

# only 1 kicker constraint
problem += pulp.lpSum(
    [kickers[kicker]["drafted_starter"] for kicker in kickers]
) == 1

# only 1 dst constraint
problem += pulp.lpSum(
    [dsts[dst]["drafted_starter"] for dst in dsts]
) == 1

# 7 bench players
problem += pulp.lpSum(
    [qbs[qb]["drafted_reserve"] for qb in qbs]
) + pulp.lpSum(
    [rbs[rb]["drafted_reserve"] for rb in rbs]
) + pulp.lpSum(
    [wrs[wr]["drafted_reserve"] for wr in wrs]
) + pulp.lpSum(
    [tes[te]["drafted_reserve"] for te in tes]
) == 7

# players can only be drafted once
for qb in qbs:
    problem += pulp.lpSum(
        [qbs[qb]["drafted_starter"], qbs[qb]["drafted_reserve"]]
    ) <= 1
for rb in rbs:
    problem += pulp.lpSum(
        [rbs[rb]["drafted_starter"], rbs[rb]["drafted_reserve"]]
    ) <= 1
for wr in wrs:
    problem += pulp.lpSum(
        [wrs[wr]["drafted_starter"], wrs[wr]["drafted_reserve"]]
    ) <= 1
for te in tes:
    problem += pulp.lpSum(
        [tes[te]["drafted_starter"], tes[te]["drafted_reserve"]]
    ) <= 1

# 1 bench qb
problem += pulp.lpSum(
    [qbs[qb]["drafted_reserve"] for qb in qbs]
) == 1

# 1 bench te
problem += pulp.lpSum(
    [tes[te]["drafted_reserve"] for te in tes]
) == 1

# remove players drafted by other teams (or players I want to avoid) from consideration
missed_qbs = [
]
missed_rbs = [
]
missed_wrs = [
]
missed_tes = []
missed_kickers = []
missed_dsts = []

for rb in missed_rbs:
    problem += rbs[rb]["drafted_starter"] == 0
    problem += rbs[rb]["drafted_reserve"] == 0


# Add Drafter Player Constraints
# problem += qbs["Joe Burrow"]["drafted_starter"] == 1

# Current player auction price
# rbs["Javonte Williams"]["avg_salary"] = 1

problem.solve()

all_players = {}
all_players.update(qbs)
all_players.update(rbs)
all_players.update(wrs)
all_players.update(tes)
all_players.update(kickers)
all_players.update(dsts)

total_salary_starters = 0
total_points_starters = 0
for player in all_players:
    if all_players[player]["drafted_starter"].value() == 1.0:
        print(f"{player} salary:{all_players[player]['avg_salary']} ppg:{all_players[player]['ppg']}")
        total_salary_starters += all_players[player]["avg_salary"]
        total_points_starters += all_players[player]["ppg"]

print(f"\nTotal Starters Salary: {total_salary_starters}")
print(f"Total Starters Points: {total_points_starters} \n")

total_salary_reserves = 0
total_points_reserves = 0
for player in all_players:
    if all_players[player]["drafted_reserve"].value() == 1.0:
        print(f"{player} salary:{all_players[player]['avg_salary']} ppg:{all_players[player]['ppg']}")
        total_salary_reserves += all_players[player]["avg_salary"]
        total_points_reserves += all_players[player]["ppg"]

print(f"\nTotal Reserves Salary: {total_salary_reserves}")
print(f"Total Reserves Points: {total_points_reserves}\n")
