def pretty_regions(keyword: str, data: dict, region_names: dict) -> str:
    """
    Форматирует региональную статистику по ключевому слову для отображения в удобочитаемом виде.

    Args:
        keyword (str): Ключевое слово, по которому собирается статистика.
        data (dict): Сырые данные о регионах из API Wordstat.
                     Ожидается структура вида:
                     {
                         "regions": [
                             {
                                 "regionId": int,       # ID региона
                                 "count": int,          # Количество запросов
                                 "share": float,        # Доля запросов в регионе
                                 "affinityIndex": float # Индекс популярности (аффинитивности)
                             },
                             ...
                         ]
                     }
        region_names (dict): Словарь сопоставления {region_id: "Название региона"}.

    Returns:
        str: Отформатированная строка со статистикой по топ-10 регионам.
             Если данных нет — возвращает сообщение "Нет данных о регионах".

    Example:
        >>> pretty_regions("купить телефон", data, {213: "Москва", 1: "Россия"})
        "📊 Региональная статистика для: 'купить телефон'\n
         📍 Топ регионов (по количеству запросов):\n
            • Москва (ID: 213) — 15 320 запросов (доля: 12.35%, индекс: 1.2)"
    """

    # Если в данных нет информации о регионах — возвращаем заглушку
    if not data or 'regions' not in data:
        return "Нет данных о регионах"

    # Заголовок блока
    result = [f"📊 Региональная статистика для: '{keyword}'"]
    result.append("\n📍 Топ регионов (по количеству запросов):")

    # Сортируем регионы по количеству запросов (от большего к меньшему)
    sorted_regions = sorted(data['regions'], key=lambda x: x['count'], reverse=True)

    # Берём только топ-10 регионов
    for region in sorted_regions[:10]:
        region_id = region['regionId']
        name = region_names.get(region_id, "Неизвестный регион")  # Название по ID
        count = f"{region['count']:,}".replace(",", " ")  # Форматируем число с пробелами
        share = region['share'] * 100  # Перевод доли в проценты
        affinity = region['affinityIndex']  # Индекс аффинитивности

        # Формируем строку по региону
        result.append(
            f"   • {name} (ID: {region_id}) — {count} запросов "
            f"(доля: {share:.2f}%, индекс: {affinity:.1f})"
        )

    # Собираем итоговый текст
    return "\n".join(result)
