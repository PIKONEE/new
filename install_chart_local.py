#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скачивает Chart.js локально и обновляет все ссылки в HTML файлах
"""

import os
import urllib.request
import ssl

project_root = '/Users/aydartleuzhanov/Desktop/InteractivePosters'
content_dir = os.path.join(project_root, 'content')
posters_dir = os.path.join(content_dir, 'posters')

print("\n" + "="*80)
print("📦 УСТАНОВКА ЛОКАЛЬНОЙ КОПИИ CHART.JS")
print("="*80 + "\n")

# Создаем папку для библиотек если её нет
libs_dir = os.path.join(content_dir, 'libs')
os.makedirs(libs_dir, exist_ok=True)

chart_js_path = os.path.join(libs_dir, 'chart.umd.min.js')

# Скачиваем Chart.js если его нет
if not os.path.exists(chart_js_path):
    print("📥 Скачиваю Chart.js...")
    chart_url = "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"
    
    try:
        # Создаем контекст SSL который игнорирует сертификаты
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(chart_url, context=context) as response:
            chart_js_code = response.read()
        
        with open(chart_js_path, 'wb') as f:
            f.write(chart_js_code)
        
        print(f"✅ Chart.js скачан: {chart_js_path}")
        print(f"   Размер: {len(chart_js_code)} байт\n")
    except Exception as e:
        print(f"❌ Ошибка при скачивании: {e}")
        print("\n💡 Попробуйте скачать вручную:")
        print("   1. Откройте: https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js")
        print(f"   2. Сохраните как: {chart_js_path}")
        exit(1)
else:
    print(f"✅ Chart.js уже есть: {chart_js_path}\n")

# Обновляем ссылки в HTML файлах
print("🔄 Обновляю ссылки в HTML файлах...\n")

cdn_patterns = [
    '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>',
    '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>',
    '<script src="https://cdn.jsdelivr.net/npm/chart.js@3"></script>',
]

# Новая локальная ссылка (относительно HTML файла)
# Например: для historykaz/kh_1.html нужно ../../libs/chart.umd.min.js
local_script = '<script src="../../libs/chart.umd.min.js"></script>'

updated = 0
total = 0

for root, dirs, files in os.walk(posters_dir):
    if 'templates' in root:
        continue
    
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    
    for filename in files:
        if filename.endswith('.html'):
            filepath = os.path.join(root, filename)
            total += 1
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Проверяем использует ли Chart
            if 'new Chart(' not in content and 'Chart(' not in content:
                continue
            
            # Заменяем CDN на локальную ссылку
            changed = False
            for pattern in cdn_patterns:
                if pattern in content:
                    content = content.replace(pattern, local_script)
                    changed = True
                    break
            
            if changed:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                rel_path = os.path.relpath(filepath, posters_dir)
                print(f"✅ {rel_path}")
                updated += 1

print("\n" + "="*80)
print(f"📊 РЕЗУЛЬТАТЫ:")
print(f"   ✅ Обновлено:   {updated} файлов")
print(f"   📝 Всего:       {total} файлов")
print(f"   📦 Библиотека:  {chart_js_path}")
print("="*80)

if updated > 0:
    print("\n🎉 ГОТОВО!")
    print("\n💡 Chart.js теперь загружается ЛОКАЛЬНО!")
    print("\n📱 ЧТО ДАЛЬШЕ:")
    print("   1. Остановите приложение")
    print("   2. Запустите снова: python3 main_app.py")
    print("   3. Откройте kh_1 - график должен работать!")
else:
    print("\n⚠️  Файлы с Chart.js не найдены")

print("="*80 + "\n")
