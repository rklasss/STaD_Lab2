import pytest
import numpy as np
from SplineInterpolator import SplineInterpolator

# 1. Тест чтения корректных данных из файла
def test_read_input_data_success():
    interpolator = SplineInterpolator()
    result = interpolator.read_input_data("tests/test_input.txt")
    assert result == ([1.0, 2.0, 3.0], [4.0, 5.0, 6.0])

# 2. Тест обработки отсутствующего файла
def test_read_input_data_file_not_found():
    interpolator = SplineInterpolator()
    result = interpolator.read_input_data("tests/non_existent.txt")
    assert result is None

# 3. Тест генерации данных по функции (x^2)
def test_read_input_data_with_function():
    interpolator = SplineInterpolator()
    result = interpolator.read_input_data("tests/test_input_x.txt", func_key=1)
    assert result == ([1.0, 2.0, 3.0], [1.0, 4.0, 9.0])

# 4. Тест некорректного количества x и y значений
def test_read_input_data_mismatched_lengths():
    interpolator = SplineInterpolator()
    result = interpolator.read_input_data("tests/test_input_mismatch.txt")
    assert result is None

# 5. Тест интерполяции в точке (положительный сценарий)
def test_interpolate_point_success():
    interpolator = SplineInterpolator()
    x_nodes = [0, 1, 2, 3]
    y_nodes = [0, 1, 4, 9]
    point = 1.5
    result = interpolator.interpolate_point(x_nodes, y_nodes, point)
    assert result is not None
    assert round(result, 2) == 2.25

# 6. Тест интерполяции вне диапазона узлов 
def test_interpolate_point_out_of_bounds():
    interpolator = SplineInterpolator()
    x_nodes = [0, 1, 2, 3]
    y_nodes = [0, 1, 4, 9]
    point = 4  
    result = interpolator.interpolate_point(x_nodes, y_nodes, point)
    assert result is not None

# 7. Тест ошибки при пустых списках узлов
def test_interpolate_point_empty_nodes():
    interpolator = SplineInterpolator()
    result = interpolator.interpolate_point([], [], 1.0)
    assert result is None

# 8. Тест успешного построения сплайна с функцией sin(x)
def test_plot_interpolation_sin():
    interpolator = SplineInterpolator()
    x_nodes = [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
    y_nodes = [0, 1, 0, -1, 0]
    interpolator.plot_interpolation(x_nodes, y_nodes, func_key=2)
    assert True 

# 9. Тест анализа чувствительности (без исключений)
def test_analyze_sensitivity():
    interpolator = SplineInterpolator()
    x_nodes = [0, 1, 2, 3]
    y_nodes = [0, 1, 4, 9]
    interpolator.analyze_sensitivity(x_nodes, y_nodes, func_key=1)
    assert True  

# 10. Тест исключений при неверных данных
def test_read_input_data_exception():
    interpolator = SplineInterpolator()
    result = interpolator.read_input_data("tests/test_input_invalid.txt")
    assert result is None
