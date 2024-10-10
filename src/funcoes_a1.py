import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Tuple, Optional
import warnings
import os
warnings.filterwarnings("ignore")

def obtem_dados_csv(path: str) -> Optional[pd.DataFrame]:
    """
    Obtem dados através de um csv. O path precisa estar especificado com um
    r na frente para indicar que o path é uma raw string

    Parameters
    ----------
    path : str
        Path do csv no computador

    Returns
    -------
    dataframe : pd.DataFrame
        Dataframe dos dados contidos no csv
        
    Examples
    --------
    >>> import pandas as pd
    >>> path = r"path_generico"
    >>> df = obtem_dados_csv(path)
    """
    try:
        # Verifica se o path passado existe
        if not os.path.exists(path):
            raise FileNotFoundError("Esse arquivo não foi encontrado.")
        else:
            # lendo os dados contidos no csv
            dataframe = pd.read_csv(path)
                
            return dataframe
    except FileNotFoundError as e:
        raise
        print(f"Erro: {e}")
        
def arrumando_dados(dataframe: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Remove dados que não são úteis e formata os dados úteis para serem
    utilizados posteriormente

    Parameters
    ----------
    dataframe : pd.DataFrame
        Dataframe que desejamos modificar

    Returns
    -------
    dataframe : pd.Dataframe
        Dataframe modificado
        
    Examples
    --------
    >>> import pandas as pd
    >>> path = r"path_generico"
    >>> df = obtem_dados_csv(path)
    >>> df_arrumado = arrumando_dados(df)
    """
    try:
        # Verificando se os tipos passados e as colunas estão conforme o esperado
        if type(dataframe) != pd.DataFrame:
            raise TypeError("o parâmetro passado precisa ser do tipo pd.DataFrame")
        if "nationality" not in dataframe.columns:
            raise KeyError("Coluna esperada inexistente no dataframe")
        if "dob" not in dataframe.columns:
            raise KeyError("Coluna esperada inexistente no dataframe")
        else:
            # selecionando as colunas que nos interessam no dataframe original
            dataframe = dataframe[["nationality", "dob"]]
                
            # convertendo dados da coluna dob para datetime, para manipular 
            # bem as datas, e depois colhendo os apenas os anos 
            dataframe["dob"] = pd.to_datetime(dataframe["dob"])
            dataframe["birth year"] = dataframe["dob"].apply(lambda x: x.year)
                
            # removendo a coluna dob
            dataframe = dataframe.drop(columns=["dob"])
                
            return dataframe
    except TypeError as e:
        raise
        print(f"Erro: {e}")
    except KeyError as e:
        raise
        print(f"Erro: {e}")

def classificando_em_periodos(dataframe_com_birth_year: pd.DataFrame, periodo: int) -> Optional[pd.DataFrame]:
    """
    Cria uma nova coluna que classifica os dados em períodos com base
    no ano de nascimento e no periodo passado

    Parameters
    ----------
    dataframe_com_birth_year : pd.DataFrame
        Dataframe que contenha uma coluna cujo nome seja "birth year"
    periodo : int
        Intervalo de tempo que desejamos classificar os períodos. Se for de 5
        em 5, passa-se 5, por exemplo

    Returns
    -------
    dataframe_com_birth_year : pd.DataFrame
        Dataframe com a coluna nova coluna que classica os dados por período
        
    Examples
    --------
    >>> import pandas as pd
    >>> path = r"path_generico"
    >>> df = obtem_dados_csv(path)
    >>> df_arrumado = arrumando_dados(df)
    >>> df_com_periodo = classificando_em_periodos(df_arrumado)

    """
    try:
        # verificando se os parametros passados são conforme o esperado
        if type(periodo) != int:
            raise TypeError("Periodo precisa ser um inteiro")
        if periodo == 0:
            raise ZeroDivisionError("O peridodo precisa ser diferente de zero")
        if periodo < 0:
            raise ValueError("O periodo deve ser positivo, pois é um intervalo de tempo")
        if type(dataframe_com_birth_year) != pd.DataFrame:
            raise TypeError("Dataframe_com_birth_year precisa ter o tipo pd.DataFrame")
        if "birth year" not in dataframe_com_birth_year.columns:
            raise KeyError("O dataframe precisa conter uma coluna inteira positiva chamada 'birth year'")
        if "nationality" not in dataframe_com_birth_year.columns:
            raise KeyError("O dataframe precisa conter uma coluna inteira positiva chamada 'nationality'")
        else:
            # classificando os anos por periodos
            dataframe_com_birth_year["period"] = (dataframe_com_birth_year["birth year"] // periodo) * periodo
                    
            return dataframe_com_birth_year
    except TypeError as e:
        raise
        print(f"Erro: {e}")
    except ZeroDivisionError as e:
        raise
        print(f"Erro: {e}")
    except ValueError as e:
        raise
        print(f"Erro: {e}")
    except KeyError as e:
        raise
        print(f"Erro: {e}")
        
        
def agrupando_nacionalidades_por_periodos_e_transformando_em_tabela(dataframe_com_period: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Dispõe dados obtidos em forma de tabela para facilitar sua operação

    Parameters
    ----------
    dataframe_com_period : pd.DataFrame
        Dataframe que possui uma coluna com períodos

    Returns
    -------
    tabela_dados : pd.DataFrame
        Dataframe com colunas com os períodos, linhas como os países e cada
        célula como a contagem
        
    Examples
    --------
    >>> import pandas as pd
    >>> path = r"path_generico"
    >>> df = obtem_dados_csv(path)
    >>> df_arrumado = arrumando_dados(df)
    >>> df_com_periodo = classificando_em_periodos(df_arrumado)
    >>> tabela = agrupando_nacionalidades_por_periodos_e_transformando_em_tabela(df_com_periodo, 10)
    """
    try:
        # Verificando se os parâmetros passados são conforme o esperado
        if type(dataframe_com_period) != pd.DataFrame:
            raise TypeError("O parametro precisa ter o tipo pd.DataFrame")
        if "nationality" not in dataframe_com_period.columns:
            raise KeyError("Coluna esperada ausente do dataframe")
        if "period" not in dataframe_com_period.columns:
            raise KeyError("Coluna esperada ausente do dataframe")
        else:
            # agrupando dados por nacionalidade e ano e depois tirando o tamanho 
            dataframe_agrupado = dataframe_com_period.groupby(["nationality", "period"]).size()
                
            # dispondo dados obtidos em tabela
            tabela_dados = dataframe_agrupado.unstack().fillna(0)
                
            return tabela_dados
    except TypeError as e:
        raise
        print(f"Erro: {e}")
    except KeyError as e:
        raise
        print(f"Erro: {e}")
        

def visualizando_pilotos_por_pais_e_periodo(tabela: pd.DataFrame, anotacoes: bool) -> None:
    """
    Visualiza a relação entre países, períodos e quantidade de pilotos nascidos

    Parameters
    ----------
    tabela : pd.DataFrame
        Tabela que contém contagem de pilotos por período e país
    anotacoes : bool
        True caso desejemos anotações que o heatmap mostre a contagem

    Returns
    -------
    None
        Apesar de não retornar nada, gera um heatmap para visualizar os dados
        
    Examples
    --------
    >>> import pandas as pd
    >>> path = r"path_generico"
    >>> df = obtem_dados_csv(path)
    >>> df_arrumado = arrumando_dados(df)
    >>> df_com_periodo = classificando_em_periodos(df_arrumado)
    >>> tabela = agrupando_nacionalidades_por_periodos_e_transformando_em_tabela(df_com_periodo, 10)
    >>> visualizando_pilotos_por_pais_e_periodo(tabela, False)
    """
    try:
        # Verificando se os parâmetros passados são conforme o esperado
        if type(tabela) != pd.DataFrame:
            raise TypeError("O tipo do parâmetro tabela precisa ser um pd.Dataframe")
        if type(anotacoes) != bool:
            raise TypeError("O tipo do parâmetro anotacoes precisa ser um bool")
        else:
            # montando um heatmap para visualizar melhor os dados
            plt.figure(figsize=(16, 10))
            sns.heatmap(tabela, annot=anotacoes, cmap="Spectral")
            plt.title("Heatmap dos pilotos nascidos por período e nacionalidade")
            plt.xlabel("Períodos")
            plt.ylabel("Países")
            plt.show()
    except TypeError as e:
        raise
        print(f"Erro: {e}")        
    
def paises_com_mais_pilotos_por_periodo(tabela: pd.DataFrame) -> Optional[Tuple[pd.Series, pd.Series]]:
    """
    Encontra a série dos países com maior nascimento de pilotos por período

    Parameters
    ----------
    tabela : pd.DataFrame
        Tabela que contém contagem de pilotos por período e país

    Returns
    -------
    pilotos_maximos_nascidos_por_periodo : pd.Series
        Série dos maiores nascimentos por período
    paises_dos_pilotos : pd.Series
        Série dos países respectivos a esses maiores nascimentos
        
    Examples
    --------
    >>> import pandas as pd
    >>> path = r"path_generico"
    >>> df = obtem_dados_csv(path)
    >>> df_arrumado = arrumando_dados(df)
    >>> df_com_periodo = classificando_em_periodos(df_arrumado)
    >>> tabela = agrupando_nacionalidades_por_periodos_e_transformando_em_tabela(df_com_periodo, 10)
    >>> pilotos_maximos_paises_e_periodo, paises_pilotos = paises_com_mais_pilotos_por_periodo(tabela)
    """
    try:
        # Verificando se os parâmetros passados são conforme o esperado
        if type(tabela) != pd.DataFrame:
            raise TypeError("O tipo do parâmetro tabela precisa ser pd.DataFrame")
        else:
            # obtendo da maior quantidade de pilotos nascidos por período
            pilotos_maximos_nascidos_por_periodo = tabela.max()
                
            # obtendo dados dos países que eles nasceram
            paises_dos_pilotos = tabela.idxmax()
                
            return pilotos_maximos_nascidos_por_periodo, paises_dos_pilotos
    except TypeError as e:
        raise
        print(f"Erro: {e}")
            

def visualizando_quais_paises_nasceram_mais_pilotos_por_periodo(pilotos_maximos_nascidos_por_periodo: pd.Series, paises_dos_pilotos: pd.Series) -> None:
    """
    Visualiza quais países nasceram mais pilotos por períodos através de um gráfico de barras

    Parameters
    ----------
    pilotos_maximos_nascidos_por_periodo : pd.Series
        Série dos maiores nascimentos por período
    paises_dos_pilotos : pd.Series
        Série dos países respectivos a esses maiores nascimentos

    Returns
    -------
    None
        Não retorna nada, mas gera um gráfico de barras onde o eixo x são os anos, 
        y a contagem de pilotos e as cores os países respectivos
        
    Examples
    --------
    >>> import pandas as pd
    >>> path = r"path_generico"
    >>> df = obtem_dados_csv(path)
    >>> df_arrumado = arrumando_dados(df)
    >>> df_com_periodo = classificando_em_periodos(df_arrumado)
    >>> tabela = agrupando_nacionalidades_por_periodos_e_transformando_em_tabela(df_com_periodo, 10)
    >>> pilotos_maximos_paises_e_periodo, paises_pilotos = paises_com_mais_pilotos_por_periodo(tabela)
    >>> visualizando_quais_paises_nasceram_mais_pilotos_por_periodo(pilotos_maximos_paises_e_periodo, paises_pilotos)
    """
    try:
        # Verificando se os parâmetros passados são conforme o esperado
        if type(pilotos_maximos_nascidos_por_periodo) != pd.Series:
            raise TypeError("Os parametros passados precisam ser pd.Series")
        if type(paises_dos_pilotos) != pd.Series:
            raise TypeError("Os parametros passados precisam ser pd.Series")
        else:
            # montando um gráfico de barras para visualizar melhor os dados
            plt.figure(figsize=(16, 10))
            sns.barplot(x=pilotos_maximos_nascidos_por_periodo.index, y=pilotos_maximos_nascidos_por_periodo, 
                            hue=paises_dos_pilotos, dodge=False)
            plt.xlabel("Anos")
            plt.ylabel("Quantidade de pilotos nascidos")
            plt.title("Maior quantidade de pilotos nascidos por período e país")
            plt.show()
    except TypeError as e:
        raise
        print(f"Erro: {e}")
        
path = r"C:\Users\jguil\Downloads\archive (11)\drivers.csv"
df = obtem_dados_csv(path)
df_arrumado = arrumando_dados(df)
df_com_periodo = classificando_em_periodos(df_arrumado, 10)
tabela = agrupando_nacionalidades_por_periodos_e_transformando_em_tabela(df_com_periodo)
pilotos_maximos_paises_e_periodo, paises_pilotos = paises_com_mais_pilotos_por_periodo(tabela)
visualizando_pilotos_por_pais_e_periodo(tabela, False)
visualizando_quais_paises_nasceram_mais_pilotos_por_periodo(pilotos_maximos_paises_e_periodo, paises_pilotos)