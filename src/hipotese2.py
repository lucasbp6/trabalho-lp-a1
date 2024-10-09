import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def search_year(year):
    filepath = "../data/races.csv"
    df = pd.read_csv(filepath)
    column_year = "year"
    column_raceId = "raceId"
    
    races = df[df[column_year] == year]
    return races[column_raceId].unique()

def filter_pit_stops(year, races):
    filepath = "../data/pit_stops.csv"
    df_pit_stops = pd.read_csv(filepath)
    column_raceId = "raceId"
    
    return df_pit_stops[df_pit_stops[column_raceId].isin(races)]

def remove_outliers(df, column, std_dev=2):
    """Remove outliers com base em desvio padrão ajustado"""
    mean = df[column].mean()
    std = df[column].std()
    
    upper_limit = mean + std_dev * std
    lower_limit = mean - std_dev * std
    
    df_cleaned = df[(df[column] >= lower_limit) & (df[column] <= upper_limit)]
    
    return df_cleaned

def associate_constructors(pit_stops_filtered):
    filepath = "../data/results.csv"
    df_results = pd.read_csv(filepath)
    column_raceId = "raceId"
    column_driverId = "driverId"
    column_constructorId = "constructorId"
    
    return pd.merge(
        pit_stops_filtered,
        df_results[[column_raceId, column_driverId, column_constructorId]],
        on=[column_raceId, column_driverId],
        how='inner'
    )

def aggregate_pit_stops(merged_df):
    column_constructorId = "constructorId"
    column_time_ms = "milliseconds"
    column_pits = "stop"
    
    return merged_df.groupby(column_constructorId).agg({
        column_time_ms: 'sum',
        column_pits: 'count'
    }).reset_index().rename(columns={column_time_ms: 'total_time_ms', column_pits: 'total_pits'})

def constructor_result(year):
    races = search_year(year)
    filepath = "../data/constructor_results.csv"
    df = pd.read_csv(filepath)
    
    column_raceId = "raceId"
    column_constructorId = "constructorId"
    column_points = "points"
    
    df_year = df[df[column_raceId].isin(races)]
    constructor_points = df_year.groupby(column_constructorId)[column_points].sum()
    
    return constructor_points

def pit_stops(year, std_dev=2):
    column_constructorId = "constructorId"
    column_pits = "pits"
    column_time = "time"

    races = search_year(year)
    pit_stops_filtered = filter_pit_stops(year, races)
    
    # Remove outliers nos tempos de pit stop com desvio padrão ajustado
    pit_stops_filtered = remove_outliers(pit_stops_filtered, "milliseconds", std_dev=std_dev)
    
    merged_df = associate_constructors(pit_stops_filtered)
    pit_stops_agg = aggregate_pit_stops(merged_df)
    
    r_result = constructor_result(year)
    final = pd.DataFrame(columns=[column_pits, column_time], index=r_result.index)

    for index, row in pit_stops_agg.iterrows():
        constructor = row[column_constructorId]
        final.loc[constructor, column_pits] = row['total_pits']
        final.loc[constructor, column_time] = row['total_time_ms']
    
    # Calcular a média de pit stop e remover as colunas 'pits' e 'time'
    final["mean_pit"] = final[column_time] / final[column_pits]
    final = final.drop(columns=[column_pits, column_time])
    
    print(final)

# Testando com desvio padrão ajustado
pit_stops(2018, std_dev=2)  # Você pode tentar 1.5 ou 1 para valores mais restritivos







