#!/usr/bin/env python3
import os
import re

def fix_html_syntax(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        script_opens = len(re.findall(r'<script[^>]*>', content))
        script_closes = len(re.findall(r'</script>', content))

        if script_opens > script_closes:
            diff = script_opens - script_closes
            for _ in range(diff):
                if '</body>' in content:
                    content = content.replace('</body>', '</script>\n</body>', 1)
                elif '</html>' in content:
                    content = content.replace('</html>', '</script>\n</html>', 1)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        return False

    except Exception as e:
        return False

def main():
    print("Исправляю синтаксические ошибки в HTML файлах...\n")
    
    fixed = 0
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.html') and 'templates' not in root:
                path = os.path.join(root, file)
                if fix_html_syntax(path):
                    print(f"✅ {path}")
                    fixed += 1
    
    print(f"\nИсправлено: {fixed}")

if __name__ == '__main__':
    main()
