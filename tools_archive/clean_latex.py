#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Удаляет все LaTeX символы и \text{} из HTML файлов
"""

import os
import re


def clean_latex(file_path):
    """Удаляет LaTeX из файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Удаляем $\text{...}$ и заменяем содержимое
        content = re.sub(r'\$\\text\{([^}]+)\}\$', r'\1', content)

        # Удаляем оставшиеся $...$
        content = re.sub(r'\$([^$]+)\$', r'\1', content)

        # Удаляем \text{...} без $
        content = re.sub(r'\\text\{([^}]+)\}', r'\1', content)

        # Удаляем другие LaTeX команды: \rightarrow и т.д.
        content = re.sub(r'\\[a-zA-Z]+', '', content)

        # Очищаем лишние пробелы
        content = re.sub(r'\s+', ' ', content)

        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"❌ Ошибка в {os.path.basename(file_path)}: {e}")
        return False


def main():
    print("🧹 Очищаю LaTeX символы из всех HTML файлов...\n")

    updated = 0

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                if clean_latex(path):
                    print(f"✅ {path}")
                    updated += 1

    print(f"\n✅ Обновлено файлов: {updated}")


if __name__ == '__main__':
    main()