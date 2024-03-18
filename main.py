#Импортируем модуль math, который предоставляет математические функции и константы
import math

#Определяем функцию circle_area, которая принимает радиус круга и возвращает площадь круга, вычисленную как произведение числа π (pi) на квадрат радиуса
def circle_area(radius):
    return math.pi * radius**2

#Определяем функцию triangle_area, которая принимает три стороны треугольника и возвращает площадь треугольника, вычисленную по формуле Герона
def triangle_area(side1, side2, side3):
    s = (side1 + side2 + side3) / 2
    area = math.sqrt(s * (s - side1) * (s - side2) * (s - side3))
    return area
#Определяем функцию is_right_triangle, которая принимает три стороны треугольника и возвращает True, если треугольник является прямоугольным, и False в противном случае
def is_right_triangle(side1, side2, side3):
    sides = [side1, side2, side3]
    max_side = max(sides)
    sides.remove(max_side)
    return max_side**2 == sides[0]**2 + sides[1]**2


#Импортируем модуль unittest для написания и запуска тестов
import unittest

#Определяем класс TestGeometry, который наследуется от unittest.TestCase для создания тестов
class TestGeometry(unittest.TestCase):

#Определяем метод test_circle_area, который проверяет правильность вычисления площади круга с радиусом 5 (с точностью до 2 знаков после запятой)
    def test_circle_area(self):
        self.assertAlmostEqual(circle_area(5), 78.54, places=2)

#Определяем метод test_triangle_area, который проверяет правильность вычисления площади треугольника с сторонами 3, 4 и 5
    def test_triangle_area(self):
        self.assertAlmostEqual(triangle_area(3, 4, 5), 6)

#Определяем метод test_is_right_triangle, который проверяет правильность определения прямоугольного треугольника для сторон 3, 4, 5  и сторон 5, 6, 7
    def test_is_right_triangle(self):
        self.assertTrue(is_right_triangle(3, 4, 5))
        self.assertFalse(is_right_triangle(5, 6, 7))

if __name__ == '__main__':
    unittest.main(argv=['ignored', '-v'], exit=False)