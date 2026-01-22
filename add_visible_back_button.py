#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Добавляет ВИДИМУЮ кнопку "Назад" в верхнюю часть всех HTML плакатов
"""

import os
import re

# HTML код для кнопки "Назад"
BACK_BUTTON_HTML = """
<!-- КНОПКА НАЗАД -->
<div style="position: fixed; top: 20px; left: 20px; z-index: 10000;">
    <button onclick="goBack()" style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        display: flex;
        align-items: center;
        gap: 8px;
    " onmouseover="this.style.transform='translateX(-3px)'; this.style.boxShadow='0 6px 20px rgba(102, 126, 234, 0.6)';" 
       onmouseout="this.style.transform='translateX(0)'; this.style.boxShadow='0 4px 15px rgba(102, 126, 234, 0.4)';">
        ← Назад
    </button>
</div>
"""

# JavaScript код для функции goBack() и QWebChannel
JAVASCRIPT_CODE = """
<script>
    function goBack() {
        if (typeof bridge !== 'undefined' && bridge) {
            bridge.onBackClicked();
        } else {
            console.log('Bridge не найден');
        }
    }

    // Инициализация QWebChannel
    if (typeof QWebChannel !== 'undefined' && typeof qt !== 'undefined') {
        try {
            new QWebChannel(qt.webChannelTransport, function(channel) {
                window.bridge = channel.objects.bridge;
                console.log('Bridge подключен');
            });
        } catch(e) {
            console.log('QWebChannel ошибка:', e);
        }
    }
</script>
"""

def add_back_button_to_file(file_path):
    """Добавляет кнопку назад и JavaScript в файл"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        modified = False

        # 1. Проверяем и добавляем кнопку, если её нет
        if '<!-- КНОПКА НАЗАД -->' not in content:
            # Ищем <body> с возможными атрибутами
            body_pattern = r'(<body[^>]*>)'
            if re.search(body_pattern, content):
                content = re.sub(body_pattern, r'\1\n' + BACK_BUTTON_HTML, content)
                modified = True
            else:
                return False, "не найден тег <body>"

        # 2. Проверяем и добавляем JavaScript, если его нет
        if 'function goBack()' not in content:
            if '</body>' in content:
                content = content.replace('</body>', JAVASCRIPT_CODE + '\n</body>')
                modified = True
            elif '</html>' in content:
                content = content.replace('</html>', JAVASCRIPT_CODE + '\n</html>')
                modified = True

        # 3. Добавляем QWebChannel script, если его нет
        if 'qwebchannel.js' not in content.lower():
            head_pattern = r'(<head[^>]*>)'
            qwebchannel_script = '\n    <script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>'
            if re.search(head_pattern, content):
                content = re.sub(head_pattern, r'\1' + qwebchannel_script, content)
                modified = True

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "обновлено"
        else:
            return False, "уже обновлено"

    except Exception as e:
        return False, f"ошибка: {str(e)}"

def main():
    print("=" * 80)
    print("🔵 ДОБАВЛЕНИЕ ВИДИМОЙ КНОПКИ 'НАЗАД' НА ВСЕ ПЛАКАТЫ")
    print("=" * 80 + "\n")

    # Ищем папку content
    content_dir = None
    for possible_path in ['content', './content', '../content']:
        if os.path.exists(possible_path):
            content_dir = possible_path
            break

    if not content_dir:
        print("❌ ОШИБКА: Папка 'content' не найдена!")
        print("   Запустите скрипт из корневой папки проекта")
        return

    print(f"📁 Найдена папка: {os.path.abspath(content_dir)}\n")

    updated = 0
    skipped = 0
    failed = 0

    # Ищем все HTML файлы в папке content/posters
    posters_dir = os.path.join(content_dir, 'posters')
    
    if not os.path.exists(posters_dir):
        print(f"❌ ОШИБКА: Папка плакатов не найдена: {posters_dir}")
        return

    print(f"🔍 Сканирую папку: {posters_dir}\n")

    for root, dirs, files in os.walk(posters_dir):
        # Пропускаем скрытые папки
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                success, message = add_back_button_to_file(path)

                # Показываем относительный путь
                rel_path = os.path.relpath(path, content_dir)
                
                if success:
                    print(f"✅ {rel_path}")
                    updated += 1
                elif "уже обновлено" in message:
                    skipped += 1
                else:
                    print(f"❌ {rel_path} - {message}")
                    failed += 1

    print("\n" + "=" * 80)
    print(f"📊 РЕЗУЛЬТАТЫ:")
    print(f"   ✅ Обновлено:  {updated} файлов")
    print(f"   ⏭️  Пропущено:  {skipped} файлов")
    print(f"   ❌ Ошибок:     {failed} файлов")
    print("=" * 80)
    
    if updated > 0:
        print("\n🎉 ГОТОВО! Кнопка 'Назад' теперь видна на всех плакатах!")
        print("   Перезапустите приложение, чтобы увидеть изменения.")
    elif skipped > 0:
        print("\n✓ Все файлы уже обновлены!")
    
    print("=" * 80)

if __name__ == '__main__':
    main()
