# -*- coding: utf-8 -*-
import os
import platform
import shutil
import subprocess
import sys


def create_icons():
    """
    Конвертирует SVG иконку в PNG, а затем в ICO для Windows.
    Возвращает путь к иконке, подходящей для текущей ОС.
    """
    try:
        import cairosvg
        from PIL import Image
    except ImportError:
        print("Ошибка: Необходимые библиотеки для создания иконок не найдены.")
        print("Пожалуйста, выполните: pip install cairosvg Pillow")
        return None

    icon_path_svg = 'icon.svg'
    icon_path_png = 'icon.png'
    icon_path_ico = 'icon.ico'
    icon_for_os = None

    if not os.path.exists(icon_path_svg):
        print(f"Ошибка: Файл иконки '{icon_path_svg}' не найден.")
        return None

    # 1. Создаем PNG из SVG
    try:
        print(f"Создание '{icon_path_png}' из SVG...")
        cairosvg.svg2png(url=icon_path_svg, write_to=icon_path_png, output_width=512, output_height=512)
    except Exception as e:
        print(f"Ошибка при создании PNG из SVG: {e}")
        return None

    # 2. Создаем ICO из PNG (только для Windows)
    if platform.system() == "Windows":
        try:
            print(f"Создание '{icon_path_ico}' для Windows...")
            img = Image.open(icon_path_png)
            img.save(icon_path_ico, format='ICO', sizes=[(256, 256)])
            icon_for_os = icon_path_ico
        except Exception as e:
            print(f"Ошибка при создании ICO: {e}")
            return None
    else:
        # Для macOS и Linux PyInstaller будет использовать PNG
        icon_for_os = icon_path_png

    print("Иконки успешно созданы.")
    return icon_for_os


def main():
    """ Главная функция сборки проекта с помощью PyInstaller. """
    app_name = "InteractivePosters"
    script_to_build = "main_app.py"

    print("--- Начало сборки приложения ---")

    icon_path = create_icons()
    if not icon_path:
        print("\nСборка прервана из-за ошибки с иконками.")
        sys.exit(1)

    # Формируем команду для PyInstaller
    pyinstaller_command = [
        'pyinstaller',
        '--noconfirm',
        '--onefile',
        '--windowed',
        f'--name={app_name}',
        '--add-data', f'content{os.pathsep}content',
        '--icon', icon_path,
        script_to_build
    ]

    print("\nЗапуск PyInstaller со следующей командой:")
    print(' '.join(pyinstaller_command))
    print("-" * 30)

    try:
        subprocess.run(pyinstaller_command, check=True)
        print("-" * 30)
        print("\nСБОРКА УСПЕШНО ЗАВЕРШЕНА!")

        # Определяем путь к готовому приложению
        dist_path = os.path.join('dist', app_name)
        if platform.system() == "Windows":
            dist_path += '.exe'
        elif platform.system() == "Darwin":
            dist_path += '.app'

        print(f"Готовое приложение находится здесь: {os.path.abspath(dist_path)}")

    except subprocess.CalledProcessError as e:
        print(f"\nОШИБКА ВО ВРЕМЯ СБОРКИ: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\nОШИБКА: команда 'pyinstaller' не найдена.")
        print("Пожалуйста, убедитесь, что вы установили все зависимости командой: pip install -r requirements.txt")
        sys.exit(1)
    finally:
        # Очистка временных файлов после сборки
        print("\nОчистка временных файлов...")
        if os.path.exists('icon.ico'): os.remove('icon.ico')
        if os.path.exists('icon.png'): os.remove('icon.png')
        if os.path.exists(f'{app_name}.spec'): os.remove(f'{app_name}.spec')
        if os.path.isdir('build'): shutil.rmtree('build')
        print("Очистка завершена.")
        print("--- Сборка приложения окончена ---")


if __name__ == "__main__":
    main()

