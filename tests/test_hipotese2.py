import pytest
import numpy as np
import pandas as pd
import sys
import os
from unittest.mock import patch
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
import hipotese2 as hip2

# Testes para search_year
def test_search_year():
    real = hip2.search_year(2023)
    print(real)
    esperado = np.array([1098, 1099, 1100, 1101, 1102, 1104, 1105, 1106, 1107, 1108, 1109, 1110,
                1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120])
    np.testing.assert_array_equal(real, esperado)
    
def test_search_year_error():
    with pytest.raises(TypeError):
        hip2.search_year('ab')

# Testes para filter_pit_stops
def test_filter_pit_stops_error():
    with pytest.raises(TypeError):
        hip2.filter_pit_stops(2023, "invalid_type")

# Testes para associate_constructors
def test_associate_constructors_error():
    with pytest.raises(TypeError):
        hip2.associate_constructors("not_a_dataframe")

# Testes para aggregate_pit_stops
def test_aggregate_pit_stops_error():
    with pytest.raises(TypeError):
        hip2.aggregate_pit_stops("not_a_dataframe")

# Testes para constructor_result
def test_constructor_result_error():
    with pytest.raises(TypeError):
        hip2.constructor_result('not_an_integer')

# Testes para pit_stops
def test_pit_stops_error():
    with pytest.raises(TypeError):
        hip2.pit_stops('invalid_year')

# Execução dos testes
pytest.main()
