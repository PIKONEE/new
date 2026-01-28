#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Удаляет кнопки "Назад" из всех HTML плакатов
"""

import os
import re

# Путь к папке с плакатами
POSTERS_PATH = r'C:\Users\Admin\PycharmProjects\pythonProject\interactive-posters\content\posters'


def remove_back_button(file_path):
    """Удаляет кнопку назад из HTML файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes = []

        # 1. Удаляем блок с кнопкой "Назад"
        button_pattern = r'<div\s+style="position:\s*fixed;\s*top:\s*20px;\s*left:\s*20px;[^"]*">\s*<button[^>]*onclick="goBack\(\)"[^>]*>.*?</button>\s*</div>'

        button_matches = re.findall(button_pattern, content, re.DOTALL | re.IGNORECASE)
        if button_matches:
            content = re.sub(button_pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
            changes.append(f"кнопка({len(button_matches)})")

        # 2. Удаляем комментарий <!-- КНОПКА НАЗАД -->
        comment_pattern = r'<!--\s*КНОПКА\s+НАЗАД\s*-->\s*'
        if re.search(comment_pattern, content, re.IGNORECASE):
            content = re.sub(comment_pattern, '', content, flags=re.IGNORECASE)
            changes.append("комментарий")

        # 3. Удаляем скрипт с function goBack()
        script_pattern = r'<script[^>]*>\s*function\s+goBack\s*\(\)[\s\S]*?</script>'

        script_matches = re.findall(script_pattern, content, re.DOTALL | re.IGNORECASE)
        if script_matches:
            content = re.sub(script_pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
            changes.append(f"скрипт({len(script_matches)})")

        # 4. Убираем дубли qwebchannel.js
        qweb_pattern = r'<script\s+type="text/javascript"\s+src="qrc:///qtwebchannel/qwebchannel\.js"></script>'
        qweb_matches = re.findall(qweb_pattern, content, re.IGNORECASE)

        if len(qweb_matches) > 1:
            head_end_match = re.search(r'</head>', content, re.IGNORECASE)
            if head_end_match:
                head_end = head_end_match.start()

                content_before_head = content[:head_end]
                content_after_head = content[head_end:]

                content_after_head = re.sub(qweb_pattern, '', content_after_head, flags=re.IGNORECASE)

                if 'qwebchannel.js' not in content_before_head.lower():
                    content_before_head = re.sub(
                        r'(</head>)',
                        r'    <script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>\n\1',
                        content_before_head,
                        count=1,
                        flags=re.IGNORECASE
                    )

                content = content_before_head + content_after_head
                changes.append(f"qweb({len(qweb_matches)}→1)")

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, ", ".join(changes)
        else:
            return False, "чистый"

    except Exception as e:
        return False, f"ошибка: {str(e)}"


def main():
    print("\n" + "=" * 80)
    print("🧹 УДАЛЕНИЕ КНОПОК 'НАЗАД' ИЗ ВСЕХ ПЛАКАТОВ")
    print("=" * 80 + "\n")

    if not os.path.exists(POSTERS_PATH):
        print(f"❌ Папка не найдена: {POSTERS_PATH}")
        return

    print(f"📁 Папка: {POSTERS_PATH}\n")

    cleaned = 0
    skipped = 0
    errors = 0
    total = 0

    # Проходим по всем папкам предметов
    for subject_folder in sorted(os.listdir(POSTERS_PATH)):
        subject_path = os.path.join(POSTERS_PATH, subject_folder)

        if not os.path.isdir(subject_path):
            continue

        print(f"\n📂 {subject_folder}/")

        # Проходим по всем HTML файлам
        html_files = [f for f in os.listdir(subject_path) if f.endswith('.html')]

        if not html_files:
            print(f"   ⚠️  Нет HTML файлов")
            continue

        for filename in sorted(html_files):
            file_path = os.path.join(subject_path, filename)
            total += 1

            success, message = remove_back_button(file_path)

            if success:
                print(f"   ✅ {filename} - {message}")
                cleaned += 1
            elif "чистый" in message:
                skipped += 1
            else:
                print(f"   ❌ {filename} - {message}")
                errors += 1

    print("\n" + "=" * 80)
    print(f"📊 РЕЗУЛЬТАТЫ:")
    print(f"   ✅ Очищено:    {cleaned} файлов")
    print(f"   ⏭️  Пропущено:  {skipped} файлов (уже чистые)")
    print(f"   ❌ Ошибок:     {errors} файлов")
    print(f"   📝 Всего:      {total} файлов")
    print("=" * 80)

    if cleaned > 0:
        print("\n🎉 ГОТОВО! Кнопки удалены из всех плакатов.")
        print("\n📱 ЧТО ДАЛЬШЕ:")
        print("   1. Проверьте несколько файлов вручную")
        print("   2. Запустите приложение")
        print("   3. Overlay-кнопка появится из main_app.py")
    elif skipped > 0:
        print("\n✓ Все файлы уже чистые!")

    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()