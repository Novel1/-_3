# Тестирование

from engine import InferenceEngine
from knowledge_base import build_rules

SCENARIOS = [
    {
        "name": "Студент с небольшим бюджетом, важна автономность",
        "facts": {"budget": "low", "primary_use": "battery", "brand_pref": "xiaomi",
                  "want_5g": "no", "storage_need": "low"},
        "expect_category": "budget_battery",
    },
    {
        "name": "Блогер, средний бюджет, приоритет камеры, бренд не важен",
        "facts": {"budget": "mid", "primary_use": "camera", "brand_pref": "any",
                  "want_5g": "yes", "storage_need": "high"},
        "expect_category": "midrange_camera",
    },
    {
        "name": "Бизнесмен с высоким бюджетом, предпочитает Apple",
        "facts": {"budget": "high", "primary_use": "business", "brand_pref": "apple",
                  "want_5g": "yes", "storage_need": "high"},
        "expect_category": "flagship_business",
    },
    {
        "name": "Геймер, средний бюджет, Samsung",
        "facts": {"budget": "mid", "primary_use": "gaming", "brand_pref": "samsung",
                  "want_5g": "no", "storage_need": "low"},
        "expect_category": "midrange_gaming",
    },
    {
        "name": "Неполные данные — без бренда и без 5G/памяти (проверка устойчивости)",
        "facts": {"budget": "low", "primary_use": "basic"},
        "expect_category": "entry_level",
    },
]


def run_all():
    ok = 0
    for i, scenario in enumerate(SCENARIOS, 1):
        engine = InferenceEngine(build_rules())
        facts = engine.run(scenario["facts"])
        passed = facts.get("category") == scenario["expect_category"]
        ok += passed
        status = "OK " if passed else "FAIL"
        print(f"[{status}] Сценарий {i}: {scenario['name']}")
        print(f"       Вход: {scenario['facts']}")
        print(f"       Категория: {facts.get('category')}  (ожидалось: {scenario['expect_category']})")
        print(f"       Линейка:   {facts.get('recommended_line', '—')}")
        if "note_5g" in facts:
            print(f"       Заметка:   {facts['note_5g']}")
        if "note_storage" in facts:
            print(f"       Заметка:   {facts['note_storage']}")
        print()
    print(f"Итог: {ok} / {len(SCENARIOS)} сценариев прошли успешно.")
    return ok == len(SCENARIOS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
