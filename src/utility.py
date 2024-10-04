from src.config import DPI, ALLOWED_EXTENSIONS


def mm_to_px(size) -> int:
    """Функция переводит мм в пиксели"""
    return int(size * (DPI / 25.4))


def get_paper_size(form) -> tuple:
    """Функция для получения ширины и высоты стандартных форматов листов"""
    paper_sizes = {
        'A2': (420, 594),
        'A3': (297, 420),
        'A4': (210, 297),
        'A5': (148, 210),
        'A6': (105, 148),
    }

    return paper_sizes[form]


def allowed_file(filename) -> bool:
    """Проверка, есть ли точка в названии файла и его расширение в списке допустимых"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
