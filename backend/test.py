import rapidfuzz
from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()
rapid = rapidfuzz.fuzz

allow = ["таблица", "схема"]
p = morph.parse("сделай таблицу")
for form in p:
    print(rapid.ratio(form.normalized, "таблица"))
