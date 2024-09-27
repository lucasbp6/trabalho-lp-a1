import pandas as pd
import numpy as np

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
    soma = 0
    race = races.max()
    champ_year = df[df[collumn_race] == race]
    #drivers = champ_year[collumn_driver].unique()
    champ_year = champ_year.sort_values(by="position")
    champ_year = champ_year[[collumn_driver, collumn_points]].set_index(collumn_driver)
    #for driver in drivers:
    #    print(champ_year[champ_year[collumn_driver]==driver][collumn_points].sum())
    #print(soma)

    return champ_year

filepath = "../data/lap_times.csv"
df = pd.read_csv(filepath)
champ_year = championship_result(2023)
print(champ_year)
drivers = champ_year.index
print(drivers)
final = pd.DataFrame(np.zeros(len(drivers), dtype=np.int32), index=drivers)
print(final)
#exit()
if False:
    collumn_ano = "nome coluna do ano"
    ano_id = "valor do ano"
    df = (df[collumn_ano] == ano_id)
    circuit_collumn = "nome da coluna com circuitos"
    tracks = df[circuit_collumn].unique()
circuit_collumn = "raceId"
collumn_driver = "driverId"
collumn_time = "milliseconds"
collumn_lap = "lap"
races = search_year(2023)
print(races)
print(df)


for track in races:
    df_btrack = (df[df[circuit_collumn] == track])
    print(df_btrack)
    laps = (df_btrack[collumn_lap].unique())
    print(laps)
   
    print(final)
    print(final.shape)
    #for car in driver:
     #   print(final.loc[car])
    
    if 1==1:
        for lap in laps:
            df_laps = (df_btrack[df_btrack[collumn_lap] == lap])
            print(df_laps)
            fast_lap = df_laps[collumn_time].argmin()
            piloto = df_laps.iloc[fast_lap].loc[collumn_driver]
            print(piloto)
            final.loc[piloto] += 1
            print(final)
            #print(fast_lap)

        


