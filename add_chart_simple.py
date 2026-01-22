#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Добавляет Chart.js во все HTML файлы в папке posters
Простой и надежный скрипт для PyCharm
"""

import os

# Путь к папке с плакатами
POSTERS_PATH = '/Users/aydartleuzhanov/Desktop/InteractivePosters/content/posters'

# Библиотека Chart.js
CHART_JS = '    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>\n'

def add_chart_to_file(filepath):
    """Добавляет Chart.js в HTML файл"""
    try:
        # Читаем файл
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем, уже есть ли Chart.js
        if 'chart.js' in content.lower():
            return False, "уже есть"
        
        # Ищем </head> и добавляем перед ним
        if '</head>' in content:
            content = content.replace('</head>', CHART_JS + '</head>')
            
            # Записываем обратно
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, "добавлен"
        else:
            return False, "нет тега </head>"
            
    except Exception as e:
        return False, f"ошибка: {e}"

def main():
    print("\n" + "="*80)
    print("📊 ДОБАВЛЕНИЕ CHART.JS ВО ВСЕ ПЛАКАТЫ")
    print("="*80 + "\n")
    
    if not os.path.exists(POSTERS_PATH):
        print(f"❌ Папка не найдена: {POSTERS_PATH}")
        print("\n💡 Проверьте путь к проекту!")
        return
    
    print(f"📁 Папка: {POSTERS_PATH}\n")
    
    # Папки с предметами
    folders = [
        'biology', 'chemistry', 'englishlang', 'geography', 
        'historykaz', 'informatics', 'kazakhlang', 'mathematics', 
        'physics', 'russianlang', 'worldhistory'
    ]
    
    added = 0
    skipped = 0
    errors = 0
    total = 0
    
    # Проходим по всем папкам
    for folder in folders:
        folder_path = os.path.join(POSTERS_PATH, folder)
        
        if not os.path.exists(folder_path):
            print(f"⚠️  Папка {folder} не найдена, пропускаю...")
            continue
        
        print(f"\n📂 {folder}/")
        
        # Проходим по всем HTML файлам в папке
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith('.html'):
                filepath = os.path.join(folder_path, filename)
                total += 1
                
                success, message = add_chart_to_file(filepath)
                
                if success:
                    print(f"   ✅ {filename} - {message}")
                    added += 1
                elif "уже есть" in message:
                    print(f"   ⏭️  {filename} - {message}")
                    skipped += 1
                else:
                    print(f"   ❌ {filename} - {message}")
                    errors += 1
    
    print("\n" + "="*80)
    print(f"📊 РЕЗУЛЬТАТЫ:")
    print(f"   ✅ Добавлено:  {added} файлов")
    print(f"   ⏭️  Пропущено:  {skipped} файлов")
    print(f"   ❌ Ошибок:     {errors} файлов")
    print(f"   📝 Всего:      {total} файлов")
    print("="*80)
    
    if added > 0:
        print("\n🎉 ГОТОВО!")
        print("\n📱 ЧТО ДАЛЬШЕ:")
        print("   1. Остановите приложение (Stop в PyCharm)")
        print("   2. Запустите снова (Run 'main_app')")
        print("   3. Откройте плакат kh_1 - ошибка исчезнет!")
    elif skipped > 0:
        print("\n✓ Chart.js уже есть во всех файлах!")
    
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
