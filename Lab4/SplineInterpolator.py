import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from typing import List, Optional, Tuple
    
# Класс для выполнения сплайн-интерполяции и анализа чувствительности данных
class SplineInterpolator:
    def __init__(self):
        self.functions = {
            1: lambda x: x**2,
            2: np.sin,
            3: np.cos,
            4: np.tan,
            5: np.abs,
            6: lambda x: np.exp(-x)
        }
        self.function_names = {
            1: "x^2",
            2: "sin(x)",
            3: "cos(x)", 
            4: "tan(x)",
            5: "|x|",
            6: "e^(-x)"
    }
        
    # Чтение входных данных из файла и генерация значений функции, если требуется
    def read_input_data(self, filename: str, func_key: Optional[int] = None) -> Optional[Tuple[List[float], List[float]]]:
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                x_values = list(map(float, lines[0].strip().split()))
                
                if len(lines) == 1 and func_key is not None:
                    y_values = [self.functions[func_key](x) for x in x_values]
                    return x_values, y_values
                
                if len(lines) >= 2:
                    y_values = list(map(float, lines[1].strip().split()))
                    
                    if len(x_values) != len(y_values):
                        print("Ошибка: количество x и y точек не совпадает")
                        return None
                    
                    return x_values, y_values
                
                print("Ошибка: недостаточно данных в файле")
                return None
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")
            return None
        
    # Вычисление значения интерполяции в заданной точке
    def interpolate_point(self, x_nodes: List[float], y_nodes: List[float], point: float) -> Optional[float]:
        try:
            spline = CubicSpline(x_nodes, y_nodes)
            return float(spline(point))
        except Exception as e:
            print(f"Ошибка интерполяции: {e}")
            return None
        
    # Построение графика интерполяции и сравнение с исходной функцией
    def plot_interpolation(self, x_nodes: List[float], y_nodes: List[float], func_key: int):
        x_smooth = np.linspace(min(x_nodes), max(x_nodes), 200)
        y_original = [self.functions[func_key](x) for x in x_smooth]
        
        spline = CubicSpline(x_nodes, y_nodes)
        y_interpolated = spline(x_smooth)
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_smooth, y_original, 'r-', label='Исходная функция')
        plt.plot(x_smooth, y_interpolated, 'b--', label='Сплайн-интерполяция')
        plt.scatter(x_nodes, y_nodes, color='green', label='Узловые точки')
        
        plt.title(f'Сплайн-интерполяция функции {self.function_names[func_key]}')
        plt.legend()
        plt.grid(True)
        
        max_deviation = max(abs(y_original[i] - y_interpolated[i]) 
                            for i in range(len(x_smooth)) 
                            if y_original[i] is not None and y_interpolated[i] is not None)
        print(f"Максимальное отклонение: {max_deviation}")
        
        plt.show()

    # Анализ чувствительности сплайна при изменении одной точки
    def analyze_sensitivity(self, x_nodes: List[float], y_nodes: List[float], func_key: int):
        original_y = y_nodes.copy()
        y_nodes[3] = 2  
        
        plt.figure(figsize=(10, 6))
        
        x_smooth = np.linspace(min(x_nodes), max(x_nodes), 200)
        
        spline_original = CubicSpline(x_nodes, original_y)
        y_original = spline_original(x_smooth)
        
        spline_modified = CubicSpline(x_nodes, y_nodes)
        y_modified = spline_modified(x_smooth)
        
        plt.plot(x_smooth, y_original, 'b-', label='Оригинальный сплайн')
        plt.plot(x_smooth, y_modified, 'r--', label='Измененный сплайн')
        plt.scatter(x_nodes, original_y, color='green')
        
        plt.title('Чувствительность сплайна')
        plt.legend()
        plt.grid(True)
        
        max_deviation = max(abs(y_original[i] - y_modified[i]) for i in range(len(x_smooth)))
        print(f"Максимальное отклонение: {max_deviation}")
        
        plt.show()
        
    # Основное меню программы для выбора действий
    def main_menu(self):
        print("Выберите действие:")
        print("1. Приближенное значение функции")
        print("2. Построение интерполяционного многочлена")
        print("3. Исследование чувствительности сплайна")
        
        try:
            choice = int(input("Введите номер действия: "))
            
            if choice == 1:
                data = self.read_input_data("input.txt")
                if not data:
                    return
                
                x_nodes, y_nodes = data
                point = float(input("Введите точку интерполяции: "))
                result = self.interpolate_point(x_nodes, y_nodes, point)
                
                if result is not None:
                    print(f"Значение в точке {point}: {result}")
            
            elif choice in [2, 3]:
                print("Выберите функцию:")
                for key, name in self.function_names.items():
                    print(f"{key}. {name}")
                
                func_key = int(input("Введите номер функции: "))
                
                data = self.read_input_data("nodes.txt", func_key)
                if not data:
                    return
                
                x_nodes, y_nodes = data
                
                if choice == 2:
                    self.plot_interpolation(x_nodes, y_nodes, func_key)
                else:
                    self.analyze_sensitivity(x_nodes, y_nodes, func_key)
        
        except ValueError:
            print("Ошибка: введите корректное число")

if __name__ == "__main__":
    interpolator = SplineInterpolator()
    interpolator.main_menu()
