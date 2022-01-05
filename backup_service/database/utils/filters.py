def leave_required_keys(filter_dict: dict, required_keys: list) -> dict:
    """
    Получить отфильтрованный по необходимым ключам словарь
    Args:
        filter_dict (dict): Словарь, который необходимо отфильтровать
        required_keys (list): Список требуемых ключей

    Returns:
        dict: Отфильтрованный словарь
    """
    return {key: value for key, value in filter_dict.items() if key in required_keys}
