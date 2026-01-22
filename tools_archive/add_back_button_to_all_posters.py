#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Добавляет ВИДИМУЮ кнопку Назад и JavaScript bridge во все HTML плакаты
Обновленная версия - теперь кнопка видна на экране!
"""

import os
import re

# HTML код для видимой кнопки "Назад"
BACK_BUTTON_HTML = """
<!-- КНОПКА НАЗАД -->
<div style="position: fixed; top: 20px; left: 20px; z-index: 10000;">
    <button onclick="goBack()" style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        padding: 12px 24px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    " onmouseover="this.style.transform='translateX(-5px)'; this.style.boxShadow='0 6px 20px rgba(102, 126, 234, 0.6)';" 
       onmouseout="this.style.transform='translateX(0)'; this.style.boxShadow='0 4px 15px rgba(102, 126, 234, 0.4)';">
        ← Назад
    </button>
</div>
"""

# JavaScript код для функции goBack() и QWebChannel
JAVASCRIPT_CODE = """
<script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>
<script>
    function goBack() {
        console.log('goBack() вызвана');
        if (typeof bridge !== 'undefined' && bridge) {
            console.log('Bridge найден, вызываю onBackClicked()');
            bridge.onBackClicked();
        } else {
            console.log('Bridge не найден!');
        }
    }

    // Инициализация QWebChannel
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Инициализация QWebChannel...');

        if (typeof QWebChannel !== 'undefined' && typeof qt !== 'undefined') {
            try {
                new QWebChannel(qt.webChannelTransport, function(channel) {
                    window.bridge = channel.objects.bridge;
                    console.log('✅ Bridge подключен!');
                });
            } catch(e) {
                console.error('❌ QWebChannel ошибка:', e);
            }
        } else {
            console.warn('⚠️ QWebChannel или qt не найден');
        }
    });
</script>
"""


def add_bridge_to_poster(file_path):
    """Добавляет видимую кнопку и JavaScript в файл плаката"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        modified = False

        # 1. Добавляем видимую кнопку, если её нет
        if '<!-- КНОПКА НАЗАД -->' not in content:
            # Ищем <body> с возможными атрибутами
            body_pattern = r'(<body[^>]*>)'
            match = re.search(body_pattern, content, re.IGNORECASE)
            if match:
                content = content.replace(match.group(1), match.group(1) + '\n' + BACK_BUTTON_HTML)
                modified = True
            else:
                return False, "не найден <body>"

        # 2. Добавляем JavaScript, если его нет
        if 'function goBack()' not in content:
            if '</body>' in content.lower():
                pos = content.lower().rfind('</body>')
                content = content[:pos] + JAVASCRIPT_CODE + '\n' + content[pos:]
                modified = True
            elif '</html>' in content.lower():
                pos = content.lower().rfind('</html>')
                content = content[:pos] + JAVASCRIPT_CODE + '\n' + content[pos:]
                modified = True
            else:
                return False, "не найден </body> или </html>"

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "добавлено"
        else:
            return False, "уже обновлено"

    except Exception as e:
        return False, f"ошибка: {str(e)}"


def main():
    print("\n" + "=" * 80)
    print("🔵 ДОБАВЛЕНИЕ ВИДИМОЙ КНОПКИ 'НАЗАД' ВО ВСЕ ПЛАКАТЫ")
    print("=" * 80 + "\n")

    updated = 0
    skipped = 0
    failed = 0

    # Подсчет файлов
    total_files = 0
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.html') and 'templates' not in root:
                total_files += 1

    print(f"📊 Найдено HTML файлов: {total_files}\n")

    current = 0
    for root, dirs, files in os.walk('.'):
        # Пропускаем скрытые папки
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if file.endswith('.html'):
                # Пропускаем файлы в templates
                if 'templates' in root:
                    continue

                current += 1
                path = os.path.join(root, file)
                success, message = add_bridge_to_poster(path)

                short_name = path.replace('./', '')

                if success:
                    print(f"[{current}/{total_files}] ✅ {short_name}")
                    updated += 1
                elif "уже обновлено" in message:
                    skipped += 1
                else:
                    print(f"[{current}/{total_files}] ❌ {short_name} - {message}")
                    failed += 1

    print("\n" + "=" * 80)
    print(f"📊 РЕЗУЛЬТАТЫ:")
    print(f"   ✅ Добавлено:   {updated} файлов")
    print(f"   ⏭️  Пропущено:   {skipped} файлов (уже были)")
    print(f"   ❌ Ошибок:      {failed} файлов")
    print(f"   📝 Всего:       {total_files} файлов")
    print("=" * 80)

    if updated > 0:
        print("\n🎉 ГОТОВО! Теперь на всех плакатах есть видимая кнопка 'Назад'!")
        print("\n📱 ЧТО ДАЛЬШЕ:")
        print("   1. Закройте приложение")
        print("   2. Запустите снова: python3 main_app.py")
        print("   3. Откройте любой плакат")
        print("   4. Увидите кнопку '← Назад' в верхнем левом углу")
    elif skipped > 0:
        print("\n✓ Все файлы уже обновлены!")
        print("   Кнопка должна быть видна на всех плакатах.")

    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()