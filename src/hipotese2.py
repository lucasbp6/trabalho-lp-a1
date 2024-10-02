import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt


def search_year(year):
    filepath = "data/races.csv" 
    df = pd.read_csv(filepath)
    column_year = "year"
    races = df[df[column_year] == year]
    return races["raceId"].unique()  


def constructor_result(year):
    races = search_year(year)
    filepath = "data/constructor_results.csv"
    df = pd.read_csv(filepath)
  
    column_race = "raceId"
    column_constructor = "constructorId"
    column_points = "points"

    df_year = df[df[column_race].isin(races)]
    
    constructor_points = df_year.groupby(column_constructor)[column_points].sum()
    
    return constructor_points

year = 2023
constructor_points = constructor_result(year)
print(f"Pontuação dos construtores no ano {year}:")
print(constructor_points)


