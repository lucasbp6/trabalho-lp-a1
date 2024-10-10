import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Union

def search_year(year: int) -> np.ndarray:
    """
    Retorna uma lista dos IDs de corridas (`raceId`) que ocorreram no ano especificado.

    :param year: Ano das corridas a serem buscadas.
    :type year: int
    :return: Array de IDs das corridas realizadas no ano especificado.
    :rtype: np.ndarray
    """
    filepath = "data/races.csv"
    df = pd.read_csv(filepath)
    column_year = "year"
    column_raceId = "raceId"
    
    races = df[df[column_year] == year]
    return races[column_raceId].unique()

def filter_pit_stops(year: int, races: np.ndarray) -> pd.DataFrame:
    """
    Filtra os pit stops correspondentes ao ano especificado.

    :param year: Ano das corridas.
    :type year: int
    :param races: IDs das corridas ocorridas no ano.
    :type races: np.ndarray
    :return: DataFrame contendo os pit stops filtrados.
    :rtype: pd.DataFrame
    """
    filepath = "data/pit_stops.csv"
    df_pit_stops = pd.read_csv(filepath)
    column_raceId = "raceId"
    column_time = "milliseconds"
    
    # Limpando os dados que por serem altos são na verdade eventos de corridas (paralizações, bandeiras vermelhas)
    df_pit_stops = df_pit_stops[df_pit_stops[column_time] < 50000]  
    return df_pit_stops[df_pit_stops[column_raceId].isin(races)]


def associate_constructors(pit_stops: pd.DataFrame) -> pd.DataFrame:
    """
    Associa os pit stops com os construtores a partir do dataset de resultados.

    :param pit_stops: DataFrame filtrado contendo os pit stops.
    :type pit_stops: pd.DataFrame
    :return: DataFrame com os pit stops associados aos construtores.
    :rtype: pd.DataFrame
    """
    filepath = "data/results.csv"
    df_results = pd.read_csv(filepath)
    column_raceId = "raceId"
    column_driverId = "driverId"
    column_constructorId = "constructorId"
    
    return pd.merge(
        pit_stops,
        df_results[[column_raceId, column_driverId, column_constructorId]],
        on=[column_raceId, column_driverId],
        how='inner'
    )

def aggregate_pit_stops(merged_df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega os dados de pit stops por construtor, somando o tempo total e o número de pit stops.

    :param merged_df: DataFrame com os pit stops e os construtores associados.
    :type merged_df: pd.DataFrame
    :return: DataFrame contendo a soma de tempos de pit stops e o total de pit stops por construtor.
    :rtype: pd.DataFrame
    """
    column_constructorId = "constructorId"
    column_time_ms = "milliseconds"
    column_pits = "stop"
    
    return merged_df.groupby(column_constructorId).agg({
        column_time_ms: 'sum',
        column_pits: 'count'
    }).reset_index().rename(columns={column_time_ms: 'total_time_ms', column_pits: 'total_pits'})

def constructor_result(year: int) -> pd.Series:
    """
    Retorna os pontos dos construtores no ano especificado.

    :param year: Ano das corridas.
    :type year: int
    :return: Série contendo os pontos acumulados pelos construtores no ano.
    :rtype: pd.Series
    """
    races = search_year(year)
    filepath = "data/constructor_results.csv"
    df = pd.read_csv(filepath)
    
    column_raceId = "raceId"
    column_constructorId = "constructorId"
    column_points = "points"
    
    df_year = df[df[column_raceId].isin(races)]
    constructor_points = df_year.groupby(column_constructorId)[column_points].sum()
    
    return constructor_points

def pit_stops(year: int) -> pd.DataFrame:
    """
    Função principal que analisa os pit stops de um determinado ano e calcula a média de tempo de pit stops por construtor.

    :param year: Ano das corridas.
    :type year: int
    :return: DataFrame contendo a média de pit stop por construtor.
    :rtype: pd.DataFrame
    """
    column_constructorId = "constructorId"
    column_pits = "pits"
    column_time = "time"

    races = search_year(year)
    pit_stops_filtered = filter_pit_stops(year, races)
    merged_df = associate_constructors(pit_stops_filtered)
    pit_stops_agg = aggregate_pit_stops(merged_df)
    
    # Obter os resultados de ponto
    r_result = constructor_result(year)
    
    # Cria um df vazio para armazenar as informações
    final = pd.DataFrame(columns=[column_pits, column_time], index=r_result.index)

    # Preenche os dados de pit stops no DataFrame
    for index, row in pit_stops_agg.iterrows():
        constructor = row[column_constructorId]
        final.loc[constructor, column_pits] = row['total_pits']
        final.loc[constructor, column_time] = row['total_time_ms']
    
    # Calcula a média de pit stop por construtora (tempo total / número de pit stops)
    final["mean_pit"] = final[column_time] / final[column_pits]
    final = final.drop(columns=[column_pits, column_time])
    
    # Exibe o resultado final
    print(final)
    return final 


a = pd.DataFrame()
# Teste da função com o ano de 2018
pits = pit_stops(2023)
real = pd.DataFrame(constructor_result(2023))
print(real)
pits = pits.sort_values(by='mean_pit')
print(pits)
real = real.sort_values(by='points', ascending=False)
print(pits, real)
df = pd.DataFrame(np.arange(len(real.index)-1,-1,-1), index=real.index)
df_pits = pd.DataFrame(np.arange(len(pits.index)-1,-1,-1), index=pits.index)
df = df.merge(df_pits, on='constructorId', how='left')
print(df)
df.plot.scatter(x='0_x', y='0_y')
plt.savefig("./")
