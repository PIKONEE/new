#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Исправляет Chart.js во ВСЕХ HTML файлах в posters
Удаляет старые версии и добавляет правильную
"""

import os

posters_path = '/Users/aydartleuzhanov/Desktop/InteractivePosters/content/posters'

print("\n" + "="*80)
print("🔧 ИСПРАВЛЕНИЕ CHART.JS ВО ВСЕХ ФАЙЛАХ")
print("="*80 + "\n")

if not os.path.exists(posters_path):
    print(f"❌ Папка не найдена: {posters_path}")
    exit(1)

print(f"📁 Папка: {posters_path}\n")

# Старые версии которые нужно удалить
old_versions = [
    '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>',
    '<script src="https://cdn.jsdelivr.net/npm/chart.js@3"></script>',
    '<script src="https://cdn.jsdelivr.net/npm/chart.js@latest"></script>',
    '<script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>',
]

# Правильная версия
correct_version = '    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>'

fixed = 0
skipped = 0
total = 0

for root, dirs, files in os.walk(posters_path):
    # Пропускаем templates
    if 'templates' in root:
        continue
    
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    
    for filename in files:
        if filename.endswith('.html'):
            filepath = os.path.join(root, filename)
            total += 1
            
            # Читаем файл
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            changed = False
            
            # Удаляем все старые версии
            for old in old_versions:
                if old in content:
                    content = content.replace(old, '')
                    changed = True
            
            # Добавляем правильную версию если её нет
            if 'chart.umd.min.js' not in content and 'chart.js@4.4.0' not in content:
                if '</head>' in content:
                    content = content.replace('</head>', correct_version + '\n</head>')
                    changed = True
            
            # Записываем если были изменения
            if changed:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                rel_path = os.path.relpath(filepath, posters_path)
                print(f"✅ {rel_path}")
                fixed += 1
            else:
                skipped += 1

print("\n" + "="*80)
print(f"📊 РЕЗУЛЬТАТЫ:")
print(f"   ✅ Исправлено:  {fixed} файлов")
print(f"   ⏭️  Пропущено:   {skipped} файлов")
print(f"   📝 Всего:       {total} файлов")
print("="*80)

if fixed > 0:
    print("\n🎉 ГОТОВО!")
    print("\n📱 ЧТО ДАЛЬШЕ:")
    print("   1. Остановите приложение (Stop в PyCharm)")
    print("   2. Запустите снова (Run 'main_app')")
    print("   3. Откройте любой плакат - ошибка исчезнет!")
elif skipped > 0:
    print("\n✓ Все файлы уже исправлены!")

print("="*80 + "\n")
