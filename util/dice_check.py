def get_score_change(dice_value: int):
    """
    Проверка на выигрышную комбинацию

    :param dice_value: значение дайса (число)
    :return: изменение счёта игрока (число)
    """

    # Совпадающие значения (кроме 777)
    if dice_value in (1, 22, 43):
        return 7, 35, 70
    # Начинающиеся с двух семёрок (опять же, не учитываем 777)
    elif dice_value in (16, 32, 48):
        return 5, 25, 50
    elif dice_value == 64:
        return 10, 50, 100
    else:
        return -1, -5, -10


def get_combo_text(dice_value: int) -> list[str]:
    """
    Возвращает то, что было на конкретном дайсе-казино
    :param dice_value: значение дайса (число)
    :return: массив строк, содержащий все выпавшие элементы в виде текста

    Альтернативный вариант:
        return [casino[(dice_value - 1) // i % 4]for i in (1, 4, 16)]
    """
    #           0       1         2        3
    values = ["BAR", "виноград", "лимон", "семь"]

    dice_value -= 1
    result = []
    for _ in range(3):
        result.append(values[dice_value % 4])
        dice_value //= 4
    return result


def get_combo_data(dice_value: int) -> tuple[tuple[int, int, int], str]:
    """
    Возвращает все необходимые для показа информации о комбинации данные

    :param dice_value: значение дайса (число)
    :return: Пара ("изменение счёта", "список выпавших элементов")
    """
    return (
        get_score_change(dice_value),
        ', '.join(get_combo_text(dice_value))
    )
