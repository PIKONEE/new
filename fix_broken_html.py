#!/usr/bin/env python3
import os
import re

def fix_broken_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем есть ли закрывающие теги
    has_head_close = '</head>' in content
    has_body_close = '</body>' in content
    has_html_close = '</html>' in content
    
    if not has_body_close or not has_html_close:
        # Добавляем недостающие теги
        if not has_body_close:
            content += '\n</body>'
        if not has_html_close:
            content += '\n</html>'
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    return False

fixed = 0
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for file in files:
        if file.endswith('.html') and 'templates' not in root:
            path = os.path.join(root, file)
            if fix_broken_html(path):
                print(f"✅ Исправлен: {path}")
                fixed += 1

print(f"\nВсего исправлено: {fixed}")
