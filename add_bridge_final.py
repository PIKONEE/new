#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

JAVASCRIPT_CODE = """<script>
    function goBack() {
        if (typeof bridge !== 'undefined' && bridge) {
            bridge.onBackClicked();
        }
    }

    if (typeof QWebChannel !== 'undefined' && typeof qt !== 'undefined') {
        try {
            new QWebChannel(qt.webChannelTransport, function(channel) {
                window.bridge = channel.objects.bridge;
            });
        } catch(e) {
            console.log('QWebChannel error:', e);
        }
    }
</script>"""

def add_bridge_to_poster(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'function goBack()' in content:
            return False, "уже обновлено"

        if '</body>' in content:
            content = content.replace('</body>', JAVASCRIPT_CODE + '\n</body>')
        elif '</html>' in content:
            content = content.replace('</html>', JAVASCRIPT_CODE + '\n</html>')
        else:
            return False, "не найден </body>"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True, "добавлено"

    except Exception as e:
        return False, f"ошибка: {str(e)}"

def main():
    print("Добавляю JavaScript для кнопки Назад...\n")

    updated = 0
    skipped = 0

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if file.endswith('.html') and 'templates' not in root:
                path = os.path.join(root, file)
                success, message = add_bridge_to_poster(path)

                if success:
                    print(f"✅ {path}")
                    updated += 1
                elif "уже обновлено" in message:
                    skipped += 1

    print(f"\nОбновлено: {updated}, Пропущено: {skipped}")

if __name__ == '__main__':
    main()
