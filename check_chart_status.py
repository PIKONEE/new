#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Проверяет статус Chart.js во всех HTML файлах
"""

import os

posters_path = '/Users/aydartleuzhanov/Desktop/InteractivePosters/content/posters'

print("\n" + "="*80)
print("📊 СТАТИСТИКА CHART.JS В ПРОЕКТЕ")
print("="*80 + "\n")

if not os.path.exists(posters_path):
    print(f"❌ Папка не найдена: {posters_path}")
    exit(1)

# Счетчики
total_html = 0
uses_chart = 0
has_local_chart = 0
has_cdn_chart = 0
no_chart = 0

files_with_issues = []

for root, dirs, files in os.walk(posters_path):
    if 'templates' in root:
        continue
    
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    
    for filename in files:
        if filename.endswith('.html'):
            filepath = os.path.join(root, filename)
            total_html += 1
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Проверяем использование Chart
            uses_chart_js = 'new Chart(' in content or 'Chart(' in content
            
            if uses_chart_js:
                uses_chart += 1
                
                # Проверяем тип подключения
                has_local = '../../libs/chart.umd.min.js' in content or '../libs/chart' in content
                has_cdn = 'cdn.jsdelivr.net/npm/chart.js' in content
                
                if has_local:
                    has_local_chart += 1
                elif has_cdn:
                    has_cdn_chart += 1
                    rel_path = os.path.relpath(filepath, posters_path)
                    files_with_issues.append((rel_path, 'CDN'))
                else:
                    rel_path = os.path.relpath(filepath, posters_path)
                    files_with_issues.append((rel_path, 'NO LIBRARY'))
            else:
                no_chart += 1

print(f"📁 Всего HTML файлов: {total_html}")
print(f"📊 Используют Chart.js: {uses_chart}")
print()
print(f"   ✅ С локальной библиотекой: {has_local_chart}")
print(f"   ⚠️  С CDN ссылкой: {has_cdn_chart}")
print(f"   ❌ Без библиотеки: {len([f for f, t in files_with_issues if t == 'NO LIBRARY'])}")
print()
print(f"📄 Не используют Chart.js: {no_chart}")

if files_with_issues:
    print("\n" + "="*80)
    print("⚠️  ФАЙЛЫ ТРЕБУЮЩИЕ ВНИМАНИЯ:")
    print("="*80)
    for filepath, issue in files_with_issues:
        print(f"   {issue}: {filepath}")

print("\n" + "="*80)

if has_local_chart == uses_chart:
    print("🎉 ВСЕ ОТЛИЧНО!")
    print("   Все файлы используют локальную библиотеку Chart.js!")
elif has_cdn_chart > 0:
    print("⚠️  ТРЕБУЕТСЯ ДЕЙСТВИЕ:")
    print(f"   {has_cdn_chart} файлов все еще используют CDN")
    print("   Запустите install_chart_local.py еще раз")
else:
    print("✓ Проверка завершена")

print("="*80 + "\n")

# Проверяем наличие самой библиотеки
libs_path = '/Users/aydartleuzhanov/Desktop/InteractivePosters/content/libs/chart.umd.min.js'
if os.path.exists(libs_path):
    size = os.path.getsize(libs_path)
    print(f"📦 Локальная библиотека Chart.js: ✅")
    print(f"   Путь: {libs_path}")
    print(f"   Размер: {size:,} байт ({size/1024:.1f} KB)")
else:
    print(f"❌ Локальная библиотека Chart.js не найдена!")
    print(f"   Ожидается: {libs_path}")

print()
