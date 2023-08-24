# gui_app settings
class GuiAppSettings:
    class Labels:
        title = {
            "text": "PDF Code Extractor",
            "font": ["Arial", 16]
        }
        choose_directory = {
            "text": "Текущая директория:"
        }
        directory = {
            "text": "Директория не выбрана",
            "bg": "white",
            "width": 50,
            "height": 2
        }
        progress = {
            "text": "Обрабатывается страница:",
            "result": "Результат сохранен в : "
        }
        file = {
            "name": "result.txt"
        }
        message = {
            "ready": "Файлы успешно распакованны!",
            "error": "Сначала укажите путь к папке с PDF!",
            "no_pdf": "В этой директории нет PDF файлов!"
        }

    class Buttons:
        browse = {
            "text": "Выбрать папку"
        }
        start_processing = {
            "text": "СТАРТ",
            "styles": {
                "background": [('active', 'lightblue')]
            }
        }

    class TextFields:
        output_text = {
            "width": 50
        }


# main settings
class MainSettings:
    APP_TITLE = "PDF Extractor"

    class Window:
        title = None
        icon_path = "path_to_icon/32px.ico"
        min_size = (600, 450)
        max_size = (600, 450)

    class About:
        name = None
        version = "1.0.0"
        author = "Alex Fedotov"
        email = "aledukar@mail.ru"

    class Menu:
        menu = "Помощь"
        title = "О программе"
        menu_name = "Название программы:"
        menu_ver = "Версия:"
        menu_autor = "Автор:"
        menu_email = "e-mail:"


# pdf_extractor settings
class PDFExtractorSettings:
    class Patterns:
        number_sequence = r"\b\d{10,18}\b"
        complex_sequence = r'^[0-9A-Za-z!"*=%<>+\-]+[A-Za-z0-9."*-=;/_]+(?=\s|$)'


MainSettings.Window.title = MainSettings.APP_TITLE
MainSettings.About.name = MainSettings.APP_TITLE
