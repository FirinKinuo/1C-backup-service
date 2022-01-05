import random
from string import ascii_lowercase


def random_string(length: int) -> str:
    """
    Генерирует строку случайных символов заданной длины
    Args:
        length (int): Длина генерируемой строки

    Returns:
        str: Сгенерированная строка
    """
    return ''.join(random.choice(ascii_lowercase) for _ in range(length))


