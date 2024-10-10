import pytest
import numpy as np
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
import hipotese1


def test_search_year():
    real = hipotese1.search_year(2023)
    print(real)
    esperado = np.array([1098, 1099, 1100, 1101, 1102, 1104, 1105, 1106, 1107, 1108, 1109, 1110,
                1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120])
    np.testing.assert_array_equal(real, esperado)

def test_search_year_error():
    with pytest.raises(TypeError):
        hipotese1.search_year('ab')

def test_search_year_error2():
    with pytest.raises(ValueError):
        hipotese1.search_year(100)

def test_championship_result():
    real = hipotese1.championship_result(2023)
    print(real)
    data = {
    'driverId': [830, 815, 1, 4, 844, 846, 832, 847, 857, 840, 
                 842, 839, 848, 852, 822, 807, 817, 855, 825, 859, 858, 856],
    'points': [575.0, 285.0, 234.0, 206.0, 206.0, 205.0, 200.0, 
               175.0, 97.0, 74.0, 62.0, 58.0, 27.0, 17.0, 10.0, 
               9.0, 6.0, 6.0, 3.0, 2.0, 1.0, 0.0]
    }
    esperado = pd.DataFrame(data).set_index('driverId')
    print(esperado)
    assert real.equals(esperado)

def test_championship_result_error():
    with pytest.raises(TypeError):
        hipotese1.championship_result('test')

def test_championship_result_error2():
    with pytest.raises(ValueError):
        hipotese1.championship_result(-10)

def test_calculate_fastest_laps():
    # ja testei as outras funcoes acima
    drivers = hipotese1.championship_result(2023).index
    races = hipotese1.search_year(2023)
    df = pd.read_csv(os.path.join(os.getcwd(),"data","lap_times.csv"))
    real = hipotese1.calculate_fastest_laps(df, drivers, races)

    data = {
    'driverId': [830, 815, 1, 4, 844, 846, 832, 847, 857, 840, 
                 842, 839, 848, 852, 822, 807, 817, 855, 825, 859, 858, 856],
    'fast': [544, 175, 86, 58, 45, 104, 46, 52, 38, 20, 
             29, 17, 8, 12, 25, 16, 10, 13, 14, 1, 9, 3]
    }
    esperado = pd.DataFrame(data).set_index('driverId')
    esperado['fast'] = esperado['fast'].astype('int32')
    pd.testing.assert_frame_equal(real, esperado)

def test_find_driver_track_err():
    real = hipotese1.find_driver_track_err(28,45)
    esperado = None
    assert real == esperado

def test_find_driver_track_err_error():
    with pytest.raises(TypeError):
        hipotese1.find_driver_track_err('ys')

def test_find_driver_tracks_err():
    with pytest.raises(ValueError):
        hipotese1.find_driver_track_err(10002, 1222)

def test_calculate_hipotesis1():
    with pytest.raises(ValueError):
        hipotese1.calculate_hipotesis(2040)

def test_calculate_hipotesis2():
    with pytest.raises(ValueError):
        hipotese1.calculate_hipotesis(10)

def test_calculate_hipotesis3():
    with pytest.raises(TypeError):
        hipotese1.calculate_hipotesis('a', 10)
        
pytest.main()
