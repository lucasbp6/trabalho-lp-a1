import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def search_year(year):
    filepath = "../data/races.csv"
    df = pd.read_csv(filepath)
    collumn_year = "year"
    races = df[df[collumn_year]==year]
    return races["raceId"].unique()

def championship_result(year):
    races = search_year(year)
    filepath = "../data/driver_standings.csv"
    df = pd.read_csv(filepath)
    collumn_race = "raceId"
    collumn_driver = "driverId"
    collumn_points = "points"
    race = races.max()
    champ_year = df[df[collumn_race] == race]
    champ_year = champ_year.sort_values(by="position")
    champ_year = champ_year[[collumn_driver, collumn_points]].set_index(collumn_driver)

    return champ_year

filepath = "../data/lap_times.csv"
df = pd.read_csv(filepath)

circuit_collumn = "raceId"
collumn_driver = "driverId"
collumn_time = "milliseconds"
collumn_lap = "lap"

champ_year = championship_result(1997)

drivers = champ_year.index
final = pd.DataFrame(np.zeros(len(drivers), dtype=np.int32), index=drivers, columns=["fast"])

races = search_year(1997)
for track in races:
    df_btrack = (df[df[circuit_collumn] == track])
    laps = (df_btrack[collumn_lap].unique())

    for lap in laps:
        df_laps = (df_btrack[df_btrack[collumn_lap] == lap])
        fast_lap = df_laps[collumn_time].argmin()
        piloto = df_laps.iloc[fast_lap].loc[collumn_driver]
        final.loc[piloto] += 1

a = final.join(champ_year, how='inner')
a.plot.scatter(x='points', y='fast', title='Relação entre Pontos e voltas rapidas', xlabel='Pontos', ylabel='voltas rapidas')
plt.show() 