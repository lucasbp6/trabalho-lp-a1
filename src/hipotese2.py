import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Union

def search_year(year: int) -> np.ndarray:
    """
    Retorna uma lista dos IDs de corridas (`raceId`) que ocorreram no ano especificado.

    Parameters
    ----------
    year : int
        Ano das corridas a serem buscadas.

    Returns
    -------
    np.ndarray
        Array de IDs das corridas realizadas no ano especificado.
        
    Exemplos
    --------
    >>> search_year(2023)
    [1098 1099 1100 1101 1102 1104 1105 1106 1107 1108 1109 1110 1111 1112
    1113 1114 1115 1116 1117 1118 1119 1120]
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

    Parameters
    ----------
    year : int
        Ano das corridas.
    races : np.ndarray
        IDs das corridas ocorridas no ano.

    Returns
    -------
    pd.DataFrame
        DataFrame contendo os pit stops filtrados.
    """
    filepath = "data/pit_stops.csv"
    df_pit_stops = pd.read_csv(filepath)
    column_raceId = "raceId"
    column_time = "milliseconds"
    
    # Limpando os dados que por serem altos são eventos como paralizações ou bandeiras vermelhas
    df_pit_stops = df_pit_stops[df_pit_stops[column_time] < 50000]  
    return df_pit_stops[df_pit_stops[column_raceId].isin(races)]


def associate_constructors(pit_stops: pd.DataFrame) -> pd.DataFrame:
    """
    Associa os pit stops com os construtores a partir do dataset de resultados.

    Parameters
    ----------
    pit_stops : pd.DataFrame
        DataFrame filtrado contendo os pit stops.

    Returns
    -------
    pd.DataFrame
        DataFrame com os pit stops associados aos construtores.
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

    Parameters
    ----------
    merged_df : pd.DataFrame
        DataFrame com os pit stops e os construtores associados.

    Returns
    -------
    pd.DataFrame
        DataFrame contendo a soma de tempos de pit stops e o total de pit stops por construtor.
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

    Parameters
    ----------
    year : int
        Ano das corridas.

    Returns
    -------
    pd.Series
        Série contendo os pontos acumulados pelos construtores no ano.
        
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

    Parameters
    ----------
    year : int
        Ano das corridas.

    Returns
    -------
    pd.DataFrame
        DataFrame contendo a média de pit stop por construtor.
    """
    column_constructorId = "constructorId"
    column_pits = "pits"
    column_time = "time"

    races = search_year(year)
    pit_stops_filtered = filter_pit_stops(year, races)
    merged_df = associate_constructors(pit_stops_filtered)
    pit_stops_agg = aggregate_pit_stops(merged_df)
    
    r_result = constructor_result(year)
    
    final = pd.DataFrame(columns=[column_pits, column_time], index=r_result.index)

    for index, row in pit_stops_agg.iterrows():
        constructor = row[column_constructorId]
        final.loc[constructor, column_pits] = row['total_pits']
        final.loc[constructor, column_time] = row['total_time_ms']
    
    final["mean_pit"] = final[column_time] / final[column_pits]
    final = final.drop(columns=[column_pits, column_time])
    
    print(final)
    return final 

def plot_scatter(combined_df: pd.DataFrame) -> None:
    """
    Gera e salva um gráfico de dispersão mostrando a relação entre a média de pit stops e os pontos dos construtores.
    
    Parameters
    ----------
    combined_df : pd.DataFrame
        DataFrame contendo as informações combinadas de pit stops e pontos.
    """
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(combined_df['mean_pit'], combined_df['points'], c=combined_df['year'], cmap='viridis', alpha=0.7)
    plt.colorbar(scatter, label='Ano')
    plt.title('Relação entre Média de Pit Stops e Pontuação dos Construtores')
    plt.xlabel('Média de Pit Stops (ms)')
    plt.ylabel('Pontuação dos Construtores')
    plt.grid(True)
    plt.savefig("scatter_pit_stops_vs_points.png")
    plt.show()


def analyze_pit_stops_across_years(start_year: int, end_year: int) -> None:
    """
    Analisa os pit stops e os pontos dos construtores ao longo de um intervalo de anos e gera o gráfico de visualização.
    
    Parameters
    ----------
    start_year : int
        Ano inicial para análise.
    end_year : int
        Ano final para análise.
    """
    all_years_data = []

    # Iterar sobre cada ano no intervalo
    for year in range(start_year, end_year + 1):
        print(f"Analisando o ano {year}...")

        # Obter os pit stops e os resultados dos construtores para o ano
        pits = pit_stops(year)
        points = pd.DataFrame(constructor_result(year), columns=['points'])
        
        # Combinar os dados de pit stops e pontos
        df_combined = pd.merge(pits, points, left_index=True, right_index=True)
        
        # Armazenar os dados de cada ano
        df_combined['year'] = year
        all_years_data.append(df_combined)

    # Concatenar os dados de todos os anos
    combined_df = pd.concat(all_years_data)
    
    # Gerar o gráfico
    plot_scatter(combined_df)

# Chamar a função para analisar os dados de 2010 a 2023
analyze_pit_stops_across_years(2010, 2023)


