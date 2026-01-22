# -*- coding: utf-8 -*-
import sys
import os
import json
import logging
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QObject, Slot, QUrl, Qt
from PySide6.QtGui import QIcon

import licensing

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONTENT_ROOT = os.path.join(BASE_DIR, 'content')


class Bridge(QObject):
    """Мост между JavaScript и Python для основной навигации"""

    def __init__(self, window):
        super().__init__()
        self.window = window

    @Slot(str)
    def onSubjectSelected(self, subject_id):
        """Пользователь выбрал предмет"""
        print(f"DEBUG: onSubjectSelected({subject_id})")
        self.window.select_subject(subject_id)

    @Slot(str)
    def onTopicClicked(self, topic_id):
        """Пользователь выбрал тему"""
        print(f"DEBUG: onTopicClicked({topic_id})")
        self.window.show_poster_screen(topic_id)

    @Slot()
    def onBackClicked(self):
        """Нажата кнопка 'Назад'"""
        print(f"DEBUG: onBackClicked()")
        self.window.go_back()

    @Slot(str)
    def onLangChanged(self, lang_code):
        """Пользователь переключил язык"""
        print(f"DEBUG: onLangChanged({lang_code})")
        self.window.change_language(lang_code)

    @Slot()
    def onFrontEndReady(self):
        """JavaScript готов получать данные"""
        print(f"DEBUG: onFrontEndReady()")
        self.window.update_content()


class ActivationBridge(QObject):
    """Мост для активации лицензии"""

    def __init__(self, window):
        super().__init__()
        self.window = window

    @Slot(str)
    def activate(self, key):
        """Активировать по ключу"""
        print(f"DEBUG: Активирую ключ: {key}")
        result, message = licensing.activate_key(key)
        if result:
            self.window.web_view.page().runJavaScript(
                "alert('Активация успешна! Приложение перезагружается.');",
                lambda: self.window.navigate_after_activation()
            )
        else:
            self.window.web_view.page().runJavaScript(f"alert('Ошибка активации: {message}');")


class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Интерактивные плакаты")
        self.setWindowIcon(QIcon(os.path.join(BASE_DIR, 'icon.svg')))

        # Переменные состояния
        self.current_lang = 'kz'
        self.current_subject = None
        self.current_screen = 'activation'  # activation, subjects, topics, poster
        self.translations = {}
        self.subjects_structure = {}

        # Построение UI
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.central_widget)

        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)

        # ВАЖНО: Разрешаем загрузку локальных файлов (для Chart.js и других библиотек)
        settings = self.web_view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        print("✅ Настройки QWebEngine: локальные файлы разрешены")

        # Построение WebChannel
        self.channel = QWebChannel()
        self.web_view.page().setWebChannel(self.channel)

        self.bridge = Bridge(self)
        self.activation_bridge = ActivationBridge(self)
        self.channel.registerObject("bridge", self.bridge)
        self.channel.registerObject("activationBridge", self.activation_bridge)

        # Загрузка данных и навигация
        self.load_all_data()
        self.navigate()

    def load_all_data(self):
        """Загружаем структуру предметов и переводы"""
        try:
            # Логирование путей
            print(f"\n{'=' * 80}")
            print(f"🔍 DEBUG ЗАГРУЗКА:")
            print(f"{'=' * 80}")
            print(f"BASE_DIR = {BASE_DIR}")
            print(f"CONTENT_ROOT = {CONTENT_ROOT}")
            print(f"CONTENT_ROOT существует: {os.path.exists(CONTENT_ROOT)}")

            if os.path.exists(CONTENT_ROOT):
                print(f"Содержимое CONTENT_ROOT:")
                for item in os.listdir(CONTENT_ROOT):
                    full_path = os.path.join(CONTENT_ROOT, item)
                    is_dir = os.path.isdir(full_path)
                    print(f"  {'📁' if is_dir else '📄'} {item}")
            print(f"{'=' * 80}\n")

            # Загружаем структуру предметов
            subjects_file = os.path.join(CONTENT_ROOT, 'subjects.json')
            print(f"📄 Путь subjects.json: {subjects_file}")
            print(f"   Существует: {os.path.exists(subjects_file)}")

            if os.path.exists(subjects_file):
                with open(subjects_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Преобразуем список в словарь для удобного доступа
                    if isinstance(data, dict) and 'subjects' in data:
                        self.subjects_structure = {s['id']: s for s in data['subjects']}
                    else:
                        self.subjects_structure = data
                print(f"   ✅ Загружено {len(self.subjects_structure)} предметов")
            else:
                print(f"   ❌ ОШИБКА: subjects.json не найден!")
                logging.error(f"Файл {subjects_file} не найден")

            # Загружаем переводы
            print(f"\n🌐 Загрузка переводов:")
            for lang in ['ru', 'kz', 'en']:
                lang_file = os.path.join(CONTENT_ROOT, 'locales', f'{lang}.json')
                print(f"   Путь {lang}.json: {lang_file}")
                print(f"      Существует: {os.path.exists(lang_file)}")

                if os.path.exists(lang_file):
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        self.translations[lang] = json.load(f)
                    print(f"      ✅ Загружен")
                else:
                    print(f"      ❌ Не найден")
                    logging.warning(f"Файл перевода {lang_file} не найден")

            print(f"\n✅ Загружены переводы: {list(self.translations.keys())}")
            print(f"{'=' * 80}\n")

            logging.info(f"Загружено {len(self.subjects_structure)} предметов")
            logging.info(f"Загружены переводы: {list(self.translations.keys())}")

        except Exception as e:
            print(f"\n❌ CRITICAL ERROR при загрузке данных:")
            print(f"   {e}")
            print(f"{'=' * 80}\n")
            logging.critical(f"Ошибка при загрузке данных: {e}", exc_info=True)

    def navigate(self):
        """Главная навигация после запуска"""
        print(f"\n🔄 navigate(): Проверяю лицензию...")
        is_activated = licensing.is_activated()
        print(f"   Лицензия активирована: {is_activated}")

        if is_activated:
            print(f"   ➜ Показываю экран выбора предметов")
            self.show_subjects_screen()
        else:
            print(f"   ➜ Показываю экран активации")
            self.show_activation_screen()

    def navigate_after_activation(self):
        """После успешной активации показываем список предметов"""
        print(f"\n✅ navigate_after_activation()")
        self.navigate()

    def show_activation_screen(self):
        """Показываем экран активации"""
        print(f"\n🖥️ show_activation_screen()")
        self.current_screen = 'activation'
        template_path = os.path.join(CONTENT_ROOT, 'templates', 'activation_screen.html')

        print(f"   Путь: {template_path}")
        print(f"   Существует: {os.path.exists(template_path)}")

        if os.path.exists(template_path):
            print(f"   ✅ Загружаю HTML")
            url = QUrl.fromLocalFile(template_path)
            self.web_view.setUrl(url)
        else:
            print(f"   ❌ Файл не найден!")
            self.web_view.setHtml(f"""
                <html>
                <head><meta charset="UTF-8"></head>
                <body style="font-family: Arial; padding: 50px; background: #f0f0f0;">
                    <h1>❌ Ошибка</h1>
                    <p>Файл активации не найден:</p>
                    <p><code>{template_path}</code></p>
                    <p>Пожалуйста, проверьте наличие файла: <code>content/templates/activation_screen.html</code></p>
                </body>
                </html>
            """)

    def show_subjects_screen(self):
        """Экран выбора предмета из 11 вариантов"""
        print(f"\n🖥️ show_subjects_screen()")
        self.current_screen = 'subjects'
        template_path = os.path.join(CONTENT_ROOT, 'templates', 'subjects_screen.html')

        print(f"   Путь: {template_path}")
        print(f"   Существует: {os.path.exists(template_path)}")

        if os.path.exists(template_path):
            print(f"   ✅ Загружаю HTML")
            url = QUrl.fromLocalFile(template_path)
            self.web_view.setUrl(url)
        else:
            print(f"   ❌ Файл не найден!")
            self.web_view.setHtml(f"""
                <html>
                <head><meta charset="UTF-8"></head>
                <body style="font-family: Arial; padding: 50px; background: #f0f0f0;">
                    <h1>❌ Ошибка</h1>
                    <p>Файл subjects_screen не найден:</p>
                    <p><code>{template_path}</code></p>
                </body>
                </html>
            """)

    def show_topics_screen(self):
        """Экран выбора темы внутри предмета"""
        print(f"\n🖥️ show_topics_screen()")
        self.current_screen = 'topics'
        template_path = os.path.join(CONTENT_ROOT, 'templates', 'topics_screen.html')

        print(f"   Путь: {template_path}")
        print(f"   Существует: {os.path.exists(template_path)}")

        if os.path.exists(template_path):
            print(f"   ✅ Загружаю HTML")
            url = QUrl.fromLocalFile(template_path)
            self.web_view.setUrl(url)
        else:
            print(f"   ❌ Файл не найден!")
            self.web_view.setHtml(f"""
                <html>
                <head><meta charset="UTF-8"></head>
                <body style="font-family: Arial; padding: 50px; background: #f0f0f0;">
                    <h1>❌ Ошибка</h1>
                    <p>Файл topics_screen не найден:</p>
                    <p><code>{template_path}</code></p>
                </body>
                </html>
            """)

    def select_subject(self, subject_id):
        """Пользователь выбрал предмет"""
        print(f"\n🎯 select_subject({subject_id})")
        if subject_id in self.subjects_structure:
            print(f"   ✅ Предмет найден")
            self.current_subject = subject_id
            subject = self.subjects_structure[subject_id]

            # Определяем язык для языковых предметов
            if subject.get('is_language_subject', False):
                lang_map = {'kazakhlang': 'kz', 'russianlang': 'ru', 'englishlang': 'en'}
                self.current_lang = lang_map.get(subject_id, 'kz')
                print(f"   🌐 Языковой предмет, язык: {self.current_lang}")
                logging.info(
                    f"Выбран языковой предмет: {subject_id}, язык: {self.current_lang}")

            self.show_topics_screen()
        else:
            print(f"   ❌ Предмет {subject_id} не найден!")
            logging.error(f"Предмет {subject_id} не найден в структуре")

    def update_content(self):
        """Обновляем содержимое текущего экрана"""
        print(f"\n📊 update_content() - текущий экран: {self.current_screen}")
        if self.current_screen == 'subjects':
            self.update_subjects_screen()
        elif self.current_screen == 'topics':
            self.update_topics_screen()

    def update_subjects_screen(self):
        """Отправляем данные всех 11 предметов на экран"""
        print(f"   📚 update_subjects_screen()")
        subjects_data = []

        for subject_id, subject in self.subjects_structure.items():
            subject_name = self._get_translation(subject.get('name_key', subject_id))
            subjects_data.append({
                'id': subject_id,
                'name': subject_name
            })

        subjects_json = json.dumps(subjects_data, ensure_ascii=False)
        js_code = f"""
            window.subjectsData = {subjects_json};
            if (typeof renderSubjects === 'function') {{
                renderSubjects(window.subjectsData);
            }}
        """
        print(f"   ✅ Отправляю {len(subjects_data)} предметов в JavaScript")
        self.web_view.page().runJavaScript(js_code)

    def update_topics_screen(self):
        """Отправляем темы выбранного предмета"""
        print(f"   📚 update_topics_screen()")
        if not self.current_subject:
            print(f"   ❌ current_subject не установлено")
            logging.error("current_subject не установлено")
            return

        subject = self.subjects_structure.get(self.current_subject)
        if not subject:
            print(f"   ❌ Предмет {self.current_subject} не найден")
            logging.error(f"Предмет {self.current_subject} не найден")
            return

        subject_name = self._get_translation(subject.get('name_key', self.current_subject))

        topics_data = []
        for topic in subject.get('topics', []):
            topic_name = topic.get('title_ru') or topic.get('name') or topic['id']
            topics_data.append({
                'id': topic['id'],
                'name': topic_name
            })

        topics_json = json.dumps(topics_data, ensure_ascii=False)
        subject_name_escaped = subject_name.replace("'", "\\'").replace('"', '\\"')
        is_lang_subject = subject.get('is_language_subject', False)

        js_code = f"""
            document.getElementById('subject-title').innerText = '{subject_name_escaped}';
            window.topicsData = {topics_json};
            window.isLangSubject = {str(is_lang_subject).lower()};

            if (typeof renderTopics === 'function') {{
                renderTopics(window.topicsData);
            }}

            // Показываем/скрываем кнопки языков
            var langControls = document.getElementById('language-controls');
            if (langControls) {{
                langControls.style.display = window.isLangSubject ? 'none' : 'flex';

                if (!window.isLangSubject) {{
                    // Устанавливаем активный язык
                    document.querySelectorAll('.lang-btn').forEach(btn => {{
                        btn.classList.remove('active');
                    }});
                    var activeLangBtn = document.getElementById('lang-{self.current_lang}');
                    if (activeLangBtn) {{
                        activeLangBtn.classList.add('active');
                    }}
                }}
            }}
        """
        print(f"   ✅ Отправляю {len(topics_data)} тем в JavaScript")
        self.web_view.page().runJavaScript(js_code)

    def show_poster_screen(self, topic_id):
        """Показываем плакат выбранной темы"""
        print(f"\n🎨 show_poster_screen({topic_id})")
        try:
            if not self.current_subject:
                print(f"   ❌ Предмет не выбран")
                logging.error("Предмет не выбран")
                return

            poster_path = os.path.join(
                CONTENT_ROOT, 'posters', self.current_subject, f"{topic_id}.html"
            )

            print(f"   Путь: {poster_path}")
            print(f"   Существует: {os.path.exists(poster_path)}")

            if os.path.exists(poster_path):
                print(f"   ✅ Загружаю плакат")
                url = QUrl.fromLocalFile(poster_path)
                url.setQuery(f"lang={self.current_lang}")
                self.web_view.setUrl(url)
                self.current_screen = 'poster'
                logging.info(
                    f"Открыт плакат: {self.current_subject}/{topic_id} на языке {self.current_lang}")
            else:
                error_msg = f"Плакат не найден: {poster_path}"
                print(f"   ❌ {error_msg}")
                logging.error(error_msg)
                self.web_view.setHtml(f"""
                    <html>
                    <head><meta charset="UTF-8"></head>
                    <body style="font-family: Arial; background: #f0f0f0; padding: 50px;">
                        <h1>❌ Ошибка</h1>
                        <p>{error_msg}</p>
                        <button onclick="if(typeof bridge !== 'undefined') bridge.onBackClicked(); else window.history.back();" 
                                style="padding: 10px 20px; font-size: 16px; cursor: pointer; background: #667eea; color: white; border: none; border-radius: 6px;">
                            ← Назад
                        </button>
                    </body>
                    </html>
                """)
        except Exception as e:
            print(f"   ❌ ОШИБКА: {e}")
            logging.error(f"Ошибка при открытии плаката: {e}", exc_info=True)
            self.web_view.setHtml(f"<h1>Ошибка: {str(e)}</h1>")

    def go_back(self):
        """Кнопка 'Назад' - возвращаемся на уровень выше"""
        print(f"\n⬅️ go_back() - текущий экран: {self.current_screen}")
        if self.current_screen == 'poster':
            print(f"   ➜ Возвращаюсь на экран тем")
            self.show_topics_screen()
            # Обновляем данные тем после загрузки
            import time
            self.web_view.page().runJavaScript(
                "setTimeout(() => { if(typeof bridge !== 'undefined') bridge.onFrontEndReady(); }, 500);")
        elif self.current_screen == 'topics':
            print(f"   ➜ Возвращаюсь на экран предметов")
            self.show_subjects_screen()
            # Обновляем данные предметов после загрузки
            import time
            self.web_view.page().runJavaScript(
                "setTimeout(() => { if(typeof bridge !== 'undefined') bridge.onFrontEndReady(); }, 500);")
        elif self.current_screen == 'subjects':
            print(f"   ➜ На главном экране, назад некуда")
            pass

    def change_language(self, lang_code):
        """Пользователь переключил язык"""
        print(f"\n🌐 change_language({lang_code})")
        if lang_code in self.translations:
            self.current_lang = lang_code
            print(f"   ✅ Язык изменен на: {lang_code}")
            logging.info(f"Язык изменен на: {lang_code}")
        else:
            print(f"   ❌ Язык {lang_code} не доступен")
            logging.warning(f"Язык {lang_code} не доступен")

    def _get_translation(self, key):
        """Получить перевод по ключу на текущем языке"""
        lang_data = self.translations.get(self.current_lang, {})

        # Если ключ - словарь (с полем 'name'), берем его
        if isinstance(lang_data.get(key), dict) and 'name' in lang_data[key]:
            return lang_data[key]['name']

        # Иначе берем строку напрямую
        return lang_data.get(key, key)


if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("🚀 ЗАПУСК ПРИЛОЖЕНИЯ 'Интерактивные плакаты'")
    print("=" * 80 + "\n")

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.resize(1280, 800)
    main_window.show()
    sys.exit(app.exec())