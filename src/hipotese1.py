import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sys
import os

def search_year(year: int) -> np.array:
    """
    Procura todas as corridas de um certo ano passado como parametros

    Parametros
    ----------
    year: int
        Indica o ano desejado
    
    Retorno
    -------
    races: numpy.array
        array com todos os id das corridas do ano
        passado como parametro
    
    Exemplo
    -------
    >>> print(search_year(2023))
    [1098 1099 1100 1101 1102 1104 1105 1106 1107 1108 1109 1110 1111 1112
     1113 1114 1115 1116 1117 1118 1119 1120]
    """
    if not isinstance(year, int):
        raise TypeError(f'{year} nao e um inteiro valido')
    if year > 2023 or year < 1950:
        raise ValueError(f'{year} esta fora do intervalo 2023-1950')
    
    #Caminho para a planilha com informacoes sobre as corridas
    filepath = os.path.join("..","data","races.csv")
    collumn_year = "year"

    df = pd.read_csv(filepath)
    #Filtra apenas as corridas de um determinado ano passado como parametro
    races = df[df[collumn_year]==year]
    races = races["raceId"].unique()
    return races

def championship_result(year: int) -> pd.DataFrame:
    """
    Busca pelo resultado real do campeonato de pilotos,
    seguindo a pontuacao oficial da categoria

    Parametros
    ---------
    year: int
        Indica o ano desejado

    Retorno
    -------
    champ_year: pd.DataFrame
        Datafreme contendo a pontuacao de cada um dos pilotos
    
    Exemplo
    -------
    >>> print(championship_result(2023))
                points
    driverId        
    830        575.0
    815        285.0
    1          234.0
    4          206.0
    844        206.0
    846        205.0
    832        200.0
    847        175.0
    857         97.0
    840         74.0
    842         62.0
    839         58.0
    848         27.0
    852         17.0
    822         10.0
    807          9.0
    817          6.0
    855          6.0
    825          3.0
    859          2.0
    858          1.0
    856          0.0
    """
    if not isinstance(year, int):
        raise TypeError(f'{year} nao e um inteiro valido')
    if year > 2023 or year < 1950:
        raise ValueError(f'{year} esta fora do intervalo 2023-1950')
    
    filepath = os.path.join("..","data","driver_standings.csv")
    collumn_race = "raceId"
    collumn_driver = "driverId"
    collumn_points = "points"

    races = search_year(year)
    df = pd.read_csv(filepath)
    #Dado um ano, busca o resultado final do campeonato, ou seja, a pontuação após a ultima corrida
    race = races.max()
    champ_year = df[df[collumn_race] == race].sort_values(by="position")
    champ_year = champ_year[[collumn_driver, collumn_points]].set_index(collumn_driver)
    return champ_year

def calculate_fastest_laps(df: pd.DataFrame, drivers: pd.Index, races: np.array) -> pd.DataFrame:
    """
    Auxilia a parte principal da hipotese, dado todas corridas
    de um ano, retorna a quantidade de voltas rapidas de cada piloto

    Parametros
    ----------
    df: pandas.DataFrame
        O dataframe com os dados de volta a volta
    drivers: pandas.Index
        Id dos pilotos participantes em um certo ano
    races: numpy.ndarray
        Id de todas as corridas de um certo ano

    Retorno:
    final pandas.DataFrame
        Retorna um DataFrame com a quantidade de voltas rapidas
        que cada piloto teve durante um ano

    Exemplos
    --------
    >>> drivers = championship_result(2023).index
    >>> races = search_year(2023)
    >>> df = pd.read_csv(os.path.join("..","data","lap_times.csv"))
    >>> print(calculate_fastest_laps(df, drivers, races))
              fast
    driverId      
    830        544
    815        175
    1           86
    4           58
    844         45
    846        104
    832         46
    847         52
    857         38
    840         20
    842         29
    839         17
    848          8
    852         12
    822         25
    807         16
    817         10
    855         13
    825         14
    859          1
    858          9
    856          3
    """
    circuit_collumn = "raceId"
    collumn_driver = "driverId"
    collumn_time = "milliseconds"
    collumn_lap = "lap"
    #Cria um dataframe de zeros com os indices dos pilotos presentes no resultado final do campeonato
    final = pd.DataFrame(np.zeros(len(drivers), dtype=np.int32), index=drivers, columns=["fast"])
    
    for track in races:
        df_btrack = (df[df[circuit_collumn] == track])
        laps = (df_btrack[collumn_lap].unique())
        for lap in laps:
            df_laps = (df_btrack[df_btrack[collumn_lap] == lap])
            fast_lap = df_laps[collumn_time].argmin()
            piloto = df_laps.iloc[fast_lap].loc[collumn_driver]
            #Para evitar erros de pilotos que fizeram alguma volta rapida, mas nao entraram na pontuacao do mundial de pilotos
            #apenas imprimo usando outra funcao e seguimos
            try:
                final.loc[piloto] += 1
            except:
                find_driver_track_err(int(piloto), int(track))

    
    return final

def find_driver_track_err(driverid: int, raceid: int) -> None:
    """
    Printa no terminal nome do piloto e informacoes da pista
    caso exista erro de ter volta mais rapida e nao tiver no 
    campeonato final

    Parametros
    ----------
    driverid: int
        Id do piloto
    raceid: int
        Id da pista

    Retorno
    -------
    None
        ela apenas imprime os valores que encontrou nas planilhas de definicao

    Exemplos
    --------
    >>> find_driver_track_err(28,45)
    forename surname
    Tarso Marques
    year  round                 name
    1996      3 Argentine Grand Prix 

    """
    if (not isinstance(driverid, int)) or (not isinstance(raceid, int)):
        raise TypeError(f'os valores nao sao inteiros')

    #Busca na base de dados com nomes dos pilotos e imprime o nome e sobrenome
    filepath = os.path.join("..", "data", "drivers.csv")
    df = pd.read_csv(filepath)

    name = df[df['driverId'] == driverid]
    if name.empty:
        raise ValueError(f'nao foi encontrado piloto com id {driverid}')
    print(name[['forename', 'surname']].to_string(index=False))
    #Busca na base de dados dos GrandPrix ano, nome e rodada em relacao ao campeonato
    filepath = os.path.join("..", "data", "races.csv")
    df = pd.read_csv(filepath)
    
    track = df[df['raceId'] == raceid]
    if track.empty:
        raise ValueError(f'nao foi encontrado grandprix com id {raceid}')
    print(track[['year', 'round', 'name']].to_string(index=False),'\n')

def calculate_hipotesis(f_year: int, l_year=None) -> pd.DataFrame:
    """
    Calcula a quantidade de voltas rapidas ano a ano no periodo dado.

    Parametros
    ----------
    f_year: int
        O primeiro ano a ser calculado (mais recente), max: 2023
    l_year: int
        O ultimo ano a ser calculado (mais antigo), min:1995
        se None => l_year = f_year (calcula apenas um ano)

    Retorno
    -------
    pandas.DataFrame
        Um dataframe com todos pilotos nesse periodo, ano a ano,
        as colunas sao o pontos feitos(% relativa ao ano)
        e quantidade de voltas rapidas(% relativa ao ano)

    Exemplo
    -------
    >>> print(calculate_hipotesis(2023, 1995))
              fast     points
    0    41.056604  23.393002
    1    13.207547  11.594793
    2     6.490566   9.519935
    3     4.377358   8.380797
    4     3.396226   8.380797
    ..         ...        ...
    662   0.000000   0.000000
    663   0.000000   0.000000
    664   0.197433   0.000000
    665   0.000000   0.000000
    666   0.000000   0.000000

    [667 rows x 2 columns]
    """
    if l_year == None:
        l_year = f_year
    if f_year > 2023:
        raise ValueError(f'Nao existem dados de voltas para anos acima de 2024')
    if l_year < 1994:
        raise ValueError(f'Nao existem dados de voltas coletados antes de 1996')
    if not isinstance(f_year, int) or not isinstance(l_year, int):
        raise TypeError(f'Os valores para limites de ano nao sao inteiros {f_year}, {l_year}')
    filepath = os.path.join("..","data","lap_times.csv")
    df = pd.read_csv(filepath)
    relacao = pd.DataFrame()
    
    for year in range(f_year, l_year, -1):
        champ_year = championship_result(year)
        drivers = champ_year.index
        races = search_year(year)
        final = calculate_fastest_laps(df, drivers, races)
        champ_year = champ_year*(100/champ_year.sum())
        final = final*(100/final.sum())
        final = final.join(champ_year, how='inner')
        relacao = pd.concat([relacao, final], ignore_index=True)
    return relacao


if __name__ == '__main__':
    relacao = calculate_hipotesis(2023, 1995)
    relacao.plot.scatter(x='points', y='fast', title='Relação entre Pontos e voltas rapidas', xlabel='Pontos (%)', ylabel='voltas rapidas (%)')
    plt.show() 