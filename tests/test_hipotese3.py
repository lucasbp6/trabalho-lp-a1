import sys
import unittest
from unittest.mock import patch
import pandas as pd
import warnings
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
import hipotese3 as f 
warnings.filterwarnings("ignore")

class Test_obtem_dados_csv(unittest.TestCase):
    
    # Fazendo o teste para o caso onde a função obtem_dados_csv funciona
    @patch("pandas.read_csv")
    @patch("os.path.exists")
    def testa_exito_obtem_dados_csv(self, mock_exists, mock_read_csv):
        mock_exists.return_value = True
        mock_dataframe = pd.DataFrame({"nationality": ["British", "German", "Spanish"], "dob": ["1985-01-07", "1977-05-10", "1985-06-27"]})
        mock_read_csv.return_value = mock_dataframe
        
        path = r"path_generico"
        dataframe = f.obtem_dados_csv(path)
        pd.testing.assert_frame_equal(dataframe, mock_dataframe)
        
        
    # Fazendo teste para a exceção FileNotFoundError
    @patch("os.path.exists")
    def testa_FileNotFoundError_obtem_dados_csv(self, mock_exists):
        # admitindo o aso onde o path passado não existe
        path = r"path_generico"
        mock_exists.return_value = False
        
        with self.assertRaises(FileNotFoundError):
            f.obtem_dados_csv(path)
            
class Test_arrumando_dados(unittest.TestCase):
    
    # Fazedo o teste para o caso onde a função arrumando_dados funciona
    def testa_exito_arruma_dados(self):
        dataframe = pd.DataFrame({"nationality": ["British", "German", "Spanish"], "dob": ["1985-01-07", "1977-05-10", "1985-06-27"]})
        
        dataframe_esperado = pd.DataFrame({"nationality": ["British", "German", "Spanish"], "birth year": [1985, 1977, 1985]})
        
        dataframe_resultante = f.arrumando_dados(dataframe)
        
        pd.testing.assert_frame_equal(dataframe_resultante, dataframe_esperado)
    
    # Fazendo o teste para o caso onde há um TypeError
    def testa_TypeError_arruma_dados(self):
        with self.assertRaises(TypeError):
            # admitindo que passamos 7 no lugar de um dataframe válido
            f.arrumando_dados(7)

    
    # Fazendo o teste para o caso onde há um KeyError
    def testa_KeyError_arruma_dados(self):
        # Admitindo que a coluna dob está faltando
        dataframe = pd.DataFrame({"nationality": ["Brazilian", "British"]})
        with self.assertRaises(KeyError):
            f.arrumando_dados(dataframe)
        
class Test_classificando_em_periodos(unittest.TestCase):
    
    # Fazendo o teste para o caso onde a função classificando_em_periodos funciona considerando um periodo de 10 anos
    def testa_exito_classificando_em_periodos(self):
        dataframe = pd.DataFrame({"nationality": ["British", "German", "Spanish"], "birth year": [1985, 1977, 1985]})
        
        dataframe_esperado = pd.DataFrame({"nationality": ["British", "German", "Spanish"], "birth year": [1985, 1977, 1985], "period": [1980, 1970, 1980]})
        
        dataframe_resultante = f.classificando_em_periodos(dataframe, 10)
        
        pd.testing.assert_frame_equal(dataframe_esperado, dataframe_resultante)
        
    # Fazendo o teste para o caso onde há um TypeError com o dataframe
    def testa_TypeError_classificando_em_periodos_1(self):
        # Admitindo que passamos um tipo errado para dataframe_com_birth_year 
        with self.assertRaises(TypeError):
            f.classificando_em_periodos("a", 10)
    
    # Fazendo o teste para o caso onde há um TypeError com o periodo
    def testa_TypeError_classicando_em_periodos_2(self):
        # Admitindo que passamso um tipo errado para periodo
        dataframe = pd.DataFrame({"nationality": ["British", "German", "Spanish"], "birth year": [1985, 1977, 1985]})
        with self.assertRaises(TypeError):
            f.classificando_em_periodos(dataframe, "a")
            
    # Fazendo o teste para o caso onde há um ZeroDivisionError com o periodo
    def testa_ZeroDivisionError_classificando_em_periodos(self):
        # Admitindo que passamos 0 como periodo
        dataframe = pd.DataFrame({"nationality": ["British", "German", "Spanish"], "birth year": [1985, 1977, 1985]})
        with self.assertRaises(ZeroDivisionError):
            f.classificando_em_periodos(dataframe, 0)
            
    # Fazendo o teste para o caso onde há um ValueError com o periodo
    def testa_ValueError_classificando_em_periodos(self):
        # Admitindo que passamos um número negativo como periodo como periodo
        dataframe = pd.DataFrame({"nationality": ["British", "German", "Spanish"], "birth year": [1985, 1977, 1985]})
        with self.assertRaises(ValueError):
            f.classificando_em_periodos(dataframe, -5)
            
    # Fazendo o teste para o caso onde há um KeyError com o periodo
    def testa_KeyError_classificando_em_periodos(self):
        # Admitindo que não existe alguma coluna esperada no dataframe
        dataframe = pd.DataFrame({"birth year": [1985, 1977, 1985]})
        with self.assertRaises(KeyError):
            f.classificando_em_periodos(dataframe, 10)
            
class Test_agrupando_nacionalidades_por_periodos_e_transformando_em_tabela(unittest.TestCase):
    
    # Testando quando a função funciona corretamente
    def testa_exito_agrupando_nacionalidades_por_periodos_e_transformando_em_tabela(self):
        dataframe = pd.DataFrame({"nationality": ["British", "German", "Spanish"], "birth year": [1985, 1977, 1985], "period": [1980, 1970, 1980]})
        
        # Criando o dataframe esperado 
        dados = {1970: [0.0, 1.0, 0.0], 1980: [1.0, 0.0, 1.0]}
        
        nationalities = ["British", "German", "Spanish"]
        
        dataframe_esperado = pd.DataFrame(dados, index=nationalities)
        
        dataframe_esperado.index.name = "nationality"
        dataframe_esperado.columns.name = "period"      
        
        # Verificando se é igual
        dataframe_gerado = f.agrupando_nacionalidades_por_periodos_e_transformando_em_tabela(dataframe)
        
        pd.testing.assert_frame_equal(dataframe_gerado, dataframe_esperado)
        
    # Fazendo o teste para o caso onde há um TypeError com o dataframe
    def testa_TypeError_agrupando_nacionalidades_por_periodos_e_transformando_em_tabela(self):
        # Admitindo que passamos um tipo errado para dataframe_com_period
        with self.assertRaises(TypeError):
            f.agrupando_nacionalidades_por_periodos_e_transformando_em_tabela("a")
        
    # Fazendo o teste para o caso onde há um KeyError com o dataframe
    def testa_KeyError_agrupando_nacionalidades_por_periodos_e_transformando_em_tabela(self):
        # Admitindo que passamos um dataframe sem uma coluna necessária para transformar em tabela
        dataframe = pd.DataFrame({"nationality": ["British", "German", "Spanish"], "birth year": [1985, 1977, 1985]})
        with self.assertRaises(KeyError):
            f.agrupando_nacionalidades_por_periodos_e_transformando_em_tabela(dataframe)
            
class Test_visualizando_pilotos_por_pais_e_periodo(unittest.TestCase):
    
    # Fazendo o teste para o caso onde um TypeError é levantado por erro na tabela
    def testa_TypeError_visualizando_pilotos_por_pais_e_periodo(self):
        # Admitindo que passamos uma parametro que não é um dataframe
        with self.assertRaises(TypeError):
            f.visualizando_pilotos_por_pais_e_periodo("a", False)
            
class Test_paises_com_mais_pilotos_por_periodo(unittest.TestCase):
    
    # Testando o caso onde a função funciona corretamente
    def testa_exito_paises_com_mais_pilotos_por_periodo(self):
        
        # Criando o dataframe
        dados = {1970: [0.0, 1.0, 0.0], 1980: [1.0, 0.0, 2.0]}
        
        nationalities = ["British", "German", "Spanish"]
        
        dataframe = pd.DataFrame(dados, index=nationalities)
        
        dataframe.index.name = "nationality"
        dataframe.columns.name = "period"  
        
        # Criando os valores esperados
        
        dados_quantidades = {1970: 1.0, 1980: 2.0}
        serie_quantidades = pd.Series(dados_quantidades)
        serie_quantidades.index.name = "period"
        
        dados_paises = {1970: "German", 1980: "Spanish"}
        serie_paises = pd.Series(dados_paises)
        serie_paises.index.name = "period"
        
        resultado_esperado = (serie_quantidades, serie_paises)
        
        # Testando se está funcionando corretamente
        
        valores_obtidos = f.paises_com_mais_pilotos_por_periodo(dataframe)
        
        pd.testing.assert_series_equal(valores_obtidos[0], resultado_esperado[0])
        pd.testing.assert_series_equal(valores_obtidos[1], resultado_esperado[1])
        
    # Testando o caso onde dá um TypeError por uma tabela passada não ser do tipo esperado
    def testa_TypeError_paises_com_mais_pilotos_por_periodo(self):
        # Admitindo que passamos uma parametro que não é um dataframe
        with self.assertRaises(TypeError):
            f.paises_com_mais_pilotos_por_periodo("a")
    
class Test_visualizando_quais_paises_nasceram_mais_pilotos_por_periodo(unittest.TestCase):
    
    # Testando caso onde passamos parâmetros de tipo inválido para a função
    def testa_TypeError_visualizando_quais_paises_nasceram_mais_pilotos_por_periodo(self):
        # Admitindo que passamos parametros errados
        with self.assertRaises(TypeError):
            f.visualizando_quais_paises_nasceram_mais_pilotos_por_periodo("a", 2)
        
        

if __name__ == "__main__":
    unittest.main()