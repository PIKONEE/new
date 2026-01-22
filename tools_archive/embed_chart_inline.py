#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Встраивает Chart.js напрямую в HTML файлы (inline)
Решает проблему с CDN и интернетом
"""

import os
import urllib.request

posters_path = '/Users/aydartleuzhanov/Desktop/InteractivePosters/content/posters'

print("\n" + "="*80)
print("📦 ВСТРАИВАНИЕ CHART.JS В HTML ФАЙЛЫ")
print("="*80 + "\n")

# Скачиваем Chart.js один раз
print("📥 Скачиваю Chart.js...")
chart_url = "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"

try:
    with urllib.request.urlopen(chart_url) as response:
        chart_js_code = response.read().decode('utf-8')
    print("✅ Chart.js скачан успешно!\n")
except Exception as e:
    print(f"❌ Ошибка при скачивании: {e}")
    print("💡 Проверьте интернет соединение")
    exit(1)

# Готовим встроенный тег
inline_chart = f'<script>\n/* Chart.js 4.4.0 - Inline */\n{chart_js_code}\n</script>'

print(f"📊 Размер Chart.js: {len(chart_js_code)} байт\n")
print("🔄 Обрабатываю файлы...\n")

fixed = 0
total = 0

for root, dirs, files in os.walk(posters_path):
    if 'templates' in root:
        continue
    
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    
    for filename in files:
        if filename.endswith('.html'):
            filepath = os.path.join(root, filename)
            total += 1
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Проверяем использует ли файл Chart
            if 'new Chart(' not in content and 'Chart(' not in content:
                continue  # Файл не использует Chart.js
            
            # Ищем и заменяем CDN ссылку на inline код
            cdn_patterns = [
                '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>',
                '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>',
                '<script src="https://cdn.jsdelivr.net/npm/chart.js@3"></script>',
            ]
            
            replaced = False
            for pattern in cdn_patterns:
                if pattern in content:
                    content = content.replace(pattern, inline_chart)
                    replaced = True
                    break
            
            # Если CDN не найден, но Chart используется - добавляем перед </head>
            if not replaced and '/* Chart.js 4.4.0 - Inline */' not in content:
                if '</head>' in content:
                    content = content.replace('</head>', inline_chart + '\n</head>')
                    replaced = True
            
            if replaced:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                rel_path = os.path.relpath(filepath, posters_path)
                print(f"✅ {rel_path}")
                fixed += 1

print("\n" + "="*80)
print(f"📊 РЕЗУЛЬТАТЫ:")
print(f"   ✅ Встроено:    {fixed} файлов")
print(f"   📝 Всего:       {total} файлов")
print("="*80)

if fixed > 0:
    print("\n🎉 ГОТОВО!")
    print("\n💡 Теперь Chart.js встроен в файлы и работает БЕЗ интернета!")
    print("\n📱 ЧТО ДАЛЬШЕ:")
    print("   1. Остановите приложение")
    print("   2. Запустите снова: python3 main_app.py")
    print("   3. Откройте kh_1 - график должен работать!")
else:
    print("\n⚠️  Файлы с Chart.js не найдены")

print("="*80 + "\n")
