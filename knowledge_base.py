from engine import Rule

QUESTIONS = [
    {
        "fact": "budget",
        "text": "Какой бюджет на покупку смартфона?",
        "options": [
            ("low", "До 100 000 тг (бюджетный)"),
            ("mid", "100 000 – 250 000 тг (средний сегмент)"),
            ("high", "Свыше 250 000 тг (флагман)"),
        ],
    },
    {
        "fact": "primary_use",
        "text": "Что для покупателя важнее всего в телефоне?",
        "options": [
            ("basic", "Звонки, мессенджеры, простые задачи"),
            ("camera", "Качество камеры и фото/видео"),
            ("gaming", "Игры и производительность"),
            ("battery", "Автономность (долгая работа без зарядки)"),
            ("business", "Статус, экосистема, деловое использование"),
        ],
    },
    {
        "fact": "brand_pref",
        "text": "Есть ли предпочтение по бренду?",
        "options": [
            ("apple", "Apple (iPhone)"),
            ("samsung", "Samsung"),
            ("xiaomi", "Xiaomi / Redmi / POCO"),
            ("any", "Без разницы — что посоветуете"),
        ],
    },
    {
        "fact": "want_5g",
        "text": "Важна ли поддержка сети 5G?",
        "options": [
            ("yes", "Да, важна"),
            ("no", "Не важна"),
        ],
    },
    {
        "fact": "storage_need",
        "text": "Сколько фото/видео/приложений планируется хранить на телефоне?",
        "options": [
            ("low", "Немного — базового объёма памяти хватит"),
            ("high", "Много — нужен большой объём встроенной памяти"),
        ],
    },
]


def build_rules():
    rules = []
    level1 = [
        (("low", "basic"), "entry_level", "малый бюджет и базовые задачи — начальный уровень"),
        (("low", "camera"), "budget_camera", "малый бюджет, но приоритет камеры — бюджетные камерофоны"),
        (("low", "gaming"), "budget_gaming", "малый бюджет, важны игры — бюджетные игровые модели"),
        (("low", "battery"), "budget_battery", "малый бюджет, важна автономность — модели с большой батареей"),
        (("low", "business"), "entry_level", "малый бюджет при деловом использовании — начальный уровень как компромисс"),

        (("mid", "basic"), "midrange", "средний бюджет и базовые задачи — средний сегмент"),
        (("mid", "camera"), "midrange_camera", "средний бюджет, приоритет камеры — камерофоны среднего сегмента"),
        (("mid", "gaming"), "midrange_gaming", "средний бюджет, важны игры — игровые модели среднего сегмента"),
        (("mid", "battery"), "midrange_battery", "средний бюджет, важна автономность"),
        (("mid", "business"), "midrange", "средний бюджет, деловое использование — средний сегмент"),

        (("high", "basic"), "flagship", "высокий бюджет — флагман даже для базовых задач"),
        (("high", "camera"), "flagship_camera", "высокий бюджет, приоритет камеры — топовые камерофоны"),
        (("high", "gaming"), "flagship_gaming", "высокий бюджет, важны игры — топовая производительность"),
        (("high", "battery"), "flagship_battery", "высокий бюджет, важна автономность — флагман с большой батареей"),
        (("high", "business"), "flagship_business", "высокий бюджет, деловое использование — премиальная линейка"),
    ]
    for (budget, use), category, expl in level1:
        rules.append(Rule(
            name=f"L1_{budget}_{use}",
            conditions={"budget": budget, "primary_use": use},
            conclusions={"category": category},
            explanation=f"Бюджет «{budget}» + сценарий «{use}»: {expl}.",
        ))

    lines_by_category = {
        "entry_level":       {"apple": "iPhone SE",              "samsung": "Samsung Galaxy A (младшие)", "xiaomi": "Redmi A / Redmi 13",        "any": "Redmi 13 или Galaxy A05"},
        "budget_camera":     {"apple": "iPhone SE",              "samsung": "Samsung Galaxy A3x",         "xiaomi": "Redmi Note (камера-версия)", "any": "Redmi Note 13 Pro"},
        "budget_gaming":     {"apple": "iPhone SE",              "samsung": "Samsung Galaxy M",            "xiaomi": "POCO X/M серии",             "any": "POCO X6"},
        "budget_battery":    {"apple": "iPhone SE",              "samsung": "Samsung Galaxy M (Monster)",  "xiaomi": "Redmi 13C / Redmi 12",       "any": "Samsung Galaxy M14"},
        "midrange":          {"apple": "iPhone 13/14",           "samsung": "Samsung Galaxy A5x",          "xiaomi": "Xiaomi 13T / Redmi Note Pro","any": "Samsung Galaxy A55"},
        "midrange_camera":   {"apple": "iPhone 13/14",           "samsung": "Samsung Galaxy A5x",          "xiaomi": "Xiaomi 13T Pro",             "any": "Xiaomi 13T Pro"},
        "midrange_gaming":   {"apple": "iPhone 13",              "samsung": "Samsung Galaxy A5x",          "xiaomi": "POCO F/X Pro серии",         "any": "POCO F6"},
        "midrange_battery":  {"apple": "iPhone 13",              "samsung": "Samsung Galaxy M5x",          "xiaomi": "Redmi Note 13 Pro+",         "any": "Samsung Galaxy M55"},
        "flagship":          {"apple": "iPhone 15",               "samsung": "Samsung Galaxy S24",         "xiaomi": "Xiaomi 14",                  "any": "Samsung Galaxy S24"},
        "flagship_camera":   {"apple": "iPhone 15 Pro / Pro Max", "samsung": "Samsung Galaxy S24 Ultra",   "xiaomi": "Xiaomi 14 Ultra",             "any": "Samsung Galaxy S24 Ultra"},
        "flagship_gaming":   {"apple": "iPhone 15 Pro",           "samsung": "Samsung Galaxy S24+",        "xiaomi": "Xiaomi 14 Pro / POCO F Pro", "any": "Samsung Galaxy S24+"},
        "flagship_battery":  {"apple": "iPhone 15 Plus",          "samsung": "Samsung Galaxy S24+",        "xiaomi": "Xiaomi 14",                  "any": "Samsung Galaxy S24+"},
        "flagship_business": {"apple": "iPhone 15 Pro Max",       "samsung": "Samsung Galaxy S24 Ultra / Z Fold", "xiaomi": "Xiaomi 14 Ultra",     "any": "iPhone 15 Pro Max"},
    }
    for category, by_brand in lines_by_category.items():
        for brand, line in by_brand.items():
            rules.append(Rule(
                name=f"L2_{category}_{brand}",
                conditions={"category": category, "brand_pref": brand},
                conclusions={"recommended_line": line},
                explanation=f"Категория «{category}» + бренд «{brand}» → линейка: {line}.",
                priority=1,
            ))
    rules.append(Rule(
        name="L3_5g",
        conditions={"want_5g": "yes"},
        conclusions={"note_5g": "Обязательно уточните у продавца-консультанта поддержку 5G у конкретной "
                                 "модификации модели перед покупкой — не все версии линейки её поддерживают."},
        explanation="Покупателю важна поддержка 5G.",
        priority=2,
    ))
    rules.append(Rule(
        name="L3_storage",
        conditions={"storage_need": "high"},
        conclusions={"note_storage": "Рекомендуется версия с памятью от 256 ГБ — учитывая объём фото/видео/приложений."},
        explanation="Покупателю нужен большой объём встроенной памяти.",
        priority=2,
    ))

    return rules
