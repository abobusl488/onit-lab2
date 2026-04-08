import unittest

class TestThatFails(unittest.TestCase):
    
    def test_that_will_fail(self):
        """Этот тест специально падает, чтобы показать что CI ловит ошибки"""
        result = 2 + 2
        self.assertEqual(result, 5, "Специальная ошибка: 2+2 не равно 5!")
    
    def test_another_fail(self):
        """Ещё один падающий тест"""
        important_value = 100
        self.assertGreater(important_value, 200, "Значение должно быть больше 200")
    
    def test_string_fail(self):
        """Тест строк"""
        name = "Lab3"
        self.assertIn("CI/CD", name, "Строка не содержит CI/CD")

if __name__ == '__main__':
    unittest.main()
