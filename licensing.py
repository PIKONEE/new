# -*- coding: utf-8 -*-
import platform
import subprocess
import hashlib
import os
import sys
from datetime import datetime

LICENSE_FILE = "license.dat"


def get_device_id():
    """ Генерирует уникальный ID на основе характеристик компьютера. """
    system = platform.system()
    if system == "Windows":
        command = "wmic csproduct get uuid"
    elif system == "Darwin":  # macOS
        command = "ioreg -d2 -c IOPlatformExpertDevice | awk -F\\\" '/IOPlatformUUID/{print $(NF-1)}'"
    else:  # Linux
        command = "cat /var/lib/dbus/machine-id"

    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL).decode().strip()
        # Извлекаем сам ID из вывода
        if system == "Windows":
            output = output.split('\n')[1].strip()
    except Exception:
        # Запасной вариант, если команда не сработала
        output = "fallback_id_for_this_machine"

    # Хешируем для анонимности и консистентности
    return hashlib.sha256(output.encode()).hexdigest()[:16].upper()


def validate_key_format(key):
    """ Проверяет, что ключ соответствует формату 'ПРЕДМЕТ-ТИП-ГОД-ЧАСТЬ1-ЧАСТЬ2'. """
    parts = key.strip().upper().split('-')
    if len(parts) != 5:
        return False, "Неверный формат ключа (требуется 5 частей).", None

    subject, key_type, year_str, part1, part2 = parts

    try:
        year = int(year_str)
        if year < datetime.now().year:
            return False, "Срок действия ключа истек.", None
    except ValueError:
        return False, "Неверный формат года в ключе.", None

    return True, "Формат корректен.", (subject.lower(), year)


def activate_key(key):
    """ Проверяет и активирует ключ, сохраняя его в файл. """
    is_valid, message, data = validate_key_format(key)
    if not is_valid:
        return False, message

    device_id = get_device_id()
    subject, year = data

    try:
        with open(LICENSE_FILE, 'w') as f:
            # Сохраняем хеш ключа, ID устройства и код предмета
            f.write(f"{hashlib.sha256(key.upper().encode()).hexdigest()}\n")
            f.write(f"{device_id}\n")
            f.write(f"{subject}\n")
        return True, "Активация прошла успешно."
    except Exception as e:
        return False, f"Не удалось сохранить файл лицензии: {e}"


def is_activated():
    """ Проверяет, активировано ли приложение на этом компьютере. """
    if not os.path.exists(LICENSE_FILE):
        return False

    try:
        with open(LICENSE_FILE, 'r') as f:
            lines = f.readlines()
            if len(lines) < 3:
                return False  # Файл поврежден

            _key_hash = lines[0].strip()
            stored_device_id = lines[1].strip()

            current_device_id = get_device_id()

            # Главная проверка: ID устройства в файле совпадает с текущим
            if stored_device_id == current_device_id:
                return True
            else:
                return False
    except Exception:
        return False


def get_activated_subject():
    """ Возвращает код предмета из файла лицензии. """
    if not is_activated():
        return None

    try:
        with open(LICENSE_FILE, 'r') as f:
            lines = f.readlines()
            return lines[2].strip()
    except Exception:
        return None

