#!/usr/bin/env python3
import os
import re

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
    } catch(e) {}
}
</script>"""

def clean_and_add(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Удаляем старые скрипты
    content = re.sub(r'<script>.*?function goBack.*?</script>', '', content, flags=re.DOTALL)
    
    # Добавляем новый
    if '</body>' in content:
        content = content.replace('</body>', JAVASCRIPT_CODE + '\n</body>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    updated = 0
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.html') and 'templates' not in root:
                path = os.path.join(root, file)
                clean_and_add(path)
                print(f"✅ {path}")
                updated += 1
    print(f"\nОбновлено: {updated}")

if __name__ == '__main__':
    main()
