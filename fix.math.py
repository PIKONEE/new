import os

# Путь к папке с плакатами по математике
TARGET_DIR = r"C:\Users\Admin\PycharmProjects\pythonProject\interactive-posters\content\posters\mathematics"

# Строка с ошибкой (как она выглядит в файле)
# Мы ищем тег с src, который не закрыт сразу, а содержит код внутри
BAD_STRING = '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js">'

# Правильная строка
# Мы закрываем тег подключения библиотеки и открываем новый тег <script> для кода
GOOD_STRING = '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>\n    <script>'


def fix_files():
    if not os.path.exists(TARGET_DIR):
        print(f"❌ Ошибка: Папка не найдена: {TARGET_DIR}")
        return

    count_fixed = 0
    count_skipped = 0

    files = os.listdir(TARGET_DIR)
    print(f"Найдено файлов в папке: {len(files)}")

    for filename in files:
        if filename.endswith(".html"):
            filepath = os.path.join(TARGET_DIR, filename)

            try:
                # Читаем файл
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Проверяем, есть ли там ошибочная строка
                if BAD_STRING in content:
                    # Заменяем на правильную
                    new_content = content.replace(BAD_STRING, GOOD_STRING)

                    # Перезаписываем файл
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                    print(f"✅ Исправлен: {filename}")
                    count_fixed += 1
                else:
                    # Если строка не найдена, возможно файл уже исправлен или там другой код
                    # print(f"➖ Пропущен (нет совпадений): {filename}")
                    count_skipped += 1

            except Exception as e:
                print(f"❌ Ошибка при обработке {filename}: {e}")

    print("-" * 40)
    print(f"🎉 Готово!")
    print(f"Исправлено файлов: {count_fixed}")
    print(f"Пропущено (уже исправлены или не нуждались): {count_skipped}")


if __name__ == "__main__":
    fix_files()