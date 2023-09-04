import pandas as pd


def get_dataframe_from_csvs():
    # Read the CSV file into a DataFrame
    df_cost = pd.read_csv('player-cost.csv', header=1)
    df_projections = pd.read_csv('player-projections.csv', header=0)

    # split the PLAYER column on whitespace, expand=True creates a dataframe
    df_cost["PLAYER"] = df_cost["PLAYER"].str.replace('\nQ\n', '\n')
    df_cost["PLAYER"] = df_cost["PLAYER"].str.replace('\n\n', '\n')
    split_cost_columns = df_cost["PLAYER"].str.split('\n', expand=True)
    df_cost["PLAYER"] = split_cost_columns[1]
    df_cost["TEAM"] = split_cost_columns[2]
    df_cost["POSITION"] = split_cost_columns[3]

    df_projections["PLAYER"] = df_projections["PLAYER"].str.replace(
        '\nQ\n', '\n')
    df_projections["PLAYER"] = df_projections["PLAYER"].str.replace(
        '\n\n', '\n')
    split_projections_columns = df_projections["PLAYER"].str.split(
        '\n', expand=True)
    df_projections["PLAYER"] = split_projections_columns[1]
    df_projections["TEAM"] = split_projections_columns[2]
    df_projections["POSITION"] = split_projections_columns[3]

    # outer join the two dataframes on the PLAYER column
    df = pd.merge(df_cost, df_projections, on='PLAYER', how='outer')

    for col in df.columns:
        print(col)

    df = df[['PLAYER', 'POSITION_x', 'TEAM_x', 'AVG', 'AVG SALARY']]
    df = df.rename(columns={
        'PLAYER': 'name',
        'POSITION_x': 'pos',
        'TEAM_x': 'team',
        'AVG': 'ppg',
        'AVG SALARY': 'avg_salary'
    })

    # filter out blank rows
    df = df[df['ppg'] > 0]
    return df

