# -*- coding: utf-8 -*-
import json
import os

KAZAKH_THEMES = [
    {"id": "kl_1", "name": "Фонетика (Әріптер мен дыбыстар)"},
    {"id": "kl_2", "name": "Сөз Құрамы (Состав слова)"},
    {"id": "kl_3", "name": "Зат Есім (Существительное)"},
    {"id": "kl_4", "name": "Ілік және Барыс Септіктері"},
    {"id": "kl_5", "name": "Қалған Септіктер (4 падежа)"},
    {"id": "kl_6", "name": "Тәуелдік Жалғау (Принадлежность)"},
    {"id": "kl_7", "name": "Сын Есім (Прилагательное)"},
    {"id": "kl_8", "name": "Есімдік (Местоимение)"},
    {"id": "kl_9", "name": "Сөз Орын Тәртібі (Порядок слов)"},
    {"id": "kl_10", "name": "Етістік және Жіктелуі"},
    {"id": "kl_11", "name": "Етістіктің Шақтары (Времена)"},
    {"id": "kl_12", "name": "Үстеу (Наречие)"},
    {"id": "kl_13", "name": "Сан Есім (Числительное)"},
    {"id": "kl_14", "name": "Шылаулар (Служебные слова)"},
    {"id": "kl_15", "name": "Сөз Тіркестері (Словосочетания)"},
    {"id": "kl_16", "name": "Бастауыш пен Баяндауыш"},
    {"id": "kl_17", "name": "Толықтауыш және Анықтауыш"},
    {"id": "kl_18", "name": "Пысықтауыш (Үстеулік Мүше)"},
    {"id": "kl_19", "name": "Қаратпа Сөздер (Обращение)"},
    {"id": "kl_20", "name": "Төл Сөз және Диалог"},
    {"id": "kl_21", "name": "Жай Сөйлем Түрлері"},
    {"id": "kl_22", "name": "Құрмалас Сөйлем"},
    {"id": "kl_23", "name": "Іс Қағаздарына Шолу"},
    {"id": "kl_24", "name": "Ресми Хабарламалар"},
    {"id": "kl_25", "name": "Қызметтік Құжаттар"},
    {"id": "kl_26", "name": "Хабарламалық Құжаттар"},
    {"id": "kl_27", "name": "Басқарушы Құжаттар"},
    {"id": "kl_28", "name": "Хат-Хабар Құжаттары"},
    {"id": "kl_29", "name": "Жеке және Хабарлау Құжаттары"},
    {"id": "kl_30", "name": "Синонимдер, Антонимдер, Омонимдер"},
    {"id": "kl_31", "name": "Фразеологизмдер"},
    {"id": "kl_32", "name": "Тыныс Белгілері (Пунктуация)"},
    {"id": "kl_33", "name": "Етіс және Етіс Түрлері (Залог)"},
    {"id": "kl_34", "name": "Етістіктің Райлары (Наклонения)"},
    {"id": "kl_35", "name": "Есімше (Причастие)"},
    {"id": "kl_36", "name": "Көсемше (Деепричастие)"},
    {"id": "kl_37", "name": "Жіктік Жалғау (Личное окончание)"},
    {"id": "kl_38", "name": "Көмекші Есімдер"},
    {"id": "kl_39", "name": "Түбір Сөзге Қосымша Жалғануы"},
    {"id": "kl_40", "name": "Сөздердің Байланысу Түрлері"},
    {"id": "kl_41", "name": "Сөйлемнің Бірыңғай Мүшелері"},
    {"id": "kl_42", "name": "Қыстырма Сөздер"},
    {"id": "kl_43", "name": "Қосымша Тыныс Белгілері"},
    {"id": "kl_44", "name": "Күрделі Сөздер және Қос Сөздер"},
    {"id": "kl_45", "name": "Дыбыстық Өзгерістер"},
    {"id": "kl_46", "name": "Үндестік Заңы"},
    {"id": "kl_47", "name": "Әдеби Тіл Нормалары"},
    {"id": "kl_48", "name": "Мәтіндік Талдау"},
]

def create_poster_html(topic_id, topic_name):
    html = f"""<!DOCTYPE html>
<html lang="kk">
<head>
    <meta charset="UTF-8">
    <title>{topic_name}</title>
    <style>
        body {{ font-family: Arial; background: #667eea; display: flex; align-items: center; justify-content: center; min-height: 100vh; }}
        .container {{ background: white; padding: 40px; border-radius: 15px; max-width: 900px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }}
        h1 {{ color: #333; margin-bottom: 20px; }}
        .back-btn {{ background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{topic_name}</h1>
        <p>Казахский язык</p>
        <button class="back-btn" onclick="history.back()">← Назад</button>
    </div>
</body>
</html>"""
    return html

with open('content/subjects.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

subjects = data.get('subjects', [])
kazakhlang = None
for s in subjects:
    if s['id'] == 'kazakhlang':
        kazakhlang = s
        break

if not kazakhlang:
    print("❌ kazakhlang не найден")
    exit(1)

kazakhlang['topics'] = KAZAKH_THEMES

with open('content/subjects.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

os.makedirs('content/posters/kazakhlang', exist_ok=True)

for theme in KAZAKH_THEMES:
    with open(f"content/posters/kazakhlang/{theme['id']}.html", 'w', encoding='utf-8') as f:
        f.write(create_poster_html(theme['id'], theme['name']))

print(f"✓ Создано {len(KAZAKH_THEMES)} плакатов")
print("✅ Готово!")
