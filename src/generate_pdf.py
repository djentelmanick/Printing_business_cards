from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
from io import BytesIO
from src.config import DPI, INDENT, STOCK, MARK_L, MARK_W, MARK_COLOR
from src.utility import mm_to_px

# Переводим настроенные параметры в пиксели
INDENT = mm_to_px(INDENT)
INIT_STOCK = STOCK
STOCK = mm_to_px(STOCK)
MARK_L = mm_to_px(MARK_L)
MARK_W = mm_to_px(MARK_W)


def draw_mark(count_hor, count_ver, right_width_bc, right_height_bc, page) -> None:
    """Функция делает маркеры для резки на листах с лицевой стороной"""
    with Drawing() as draw:
        # Устанавливаем цвет и толщину линии
        draw.stroke_color = Color(MARK_COLOR)
        draw.stroke_width = MARK_W

        for ind_mark in range(count_hor + 1):
            if ind_mark == 0:
                draw.line((INDENT + ind_mark * right_width_bc + STOCK, INDENT - MARK_L),
                          (INDENT + ind_mark * right_width_bc + STOCK, INDENT))

                draw.line((INDENT + ind_mark * right_width_bc + STOCK, INDENT + MARK_L + count_ver * right_height_bc),
                          (INDENT + ind_mark * right_width_bc + STOCK, INDENT + count_ver * right_height_bc))
            elif ind_mark == count_hor:
                draw.line((INDENT + ind_mark * right_width_bc - STOCK, INDENT - MARK_L),
                          (INDENT + ind_mark * right_width_bc - STOCK, INDENT))

                draw.line((INDENT + ind_mark * right_width_bc - STOCK, INDENT + MARK_L + count_ver * right_height_bc),
                          (INDENT + ind_mark * right_width_bc - STOCK, INDENT + count_ver * right_height_bc))
            else:
                draw.line((INDENT + ind_mark * right_width_bc - STOCK, INDENT - MARK_L),
                          (INDENT + ind_mark * right_width_bc - STOCK, INDENT))
                draw.line((INDENT + ind_mark * right_width_bc + STOCK, INDENT - MARK_L),
                          (INDENT + ind_mark * right_width_bc + STOCK, INDENT))

                draw.line((INDENT + ind_mark * right_width_bc + STOCK, INDENT + MARK_L + count_ver * right_height_bc),
                          (INDENT + ind_mark * right_width_bc + STOCK, INDENT + count_ver * right_height_bc))
                draw.line((INDENT + ind_mark * right_width_bc - STOCK, INDENT + MARK_L + count_ver * right_height_bc),
                          (INDENT + ind_mark * right_width_bc - STOCK, INDENT + count_ver * right_height_bc))

        for ind_mark in range(count_ver + 1):
            if ind_mark == 0:
                draw.line((INDENT - MARK_L, INDENT + STOCK + ind_mark * right_height_bc),
                          (INDENT, INDENT + STOCK + ind_mark * right_height_bc))

                draw.line((INDENT + MARK_L + count_hor * right_width_bc, INDENT + STOCK + ind_mark * right_height_bc),
                          (INDENT + count_hor * right_width_bc, INDENT + STOCK + ind_mark * right_height_bc))
            elif ind_mark == count_ver:
                draw.line((INDENT - MARK_L, INDENT - STOCK + ind_mark * right_height_bc),
                          (INDENT, INDENT - STOCK + ind_mark * right_height_bc))

                draw.line((INDENT + MARK_L + count_hor * right_width_bc, INDENT - STOCK + ind_mark * right_height_bc),
                          (INDENT + count_hor * right_width_bc, INDENT - STOCK + ind_mark * right_height_bc))
            else:
                draw.line((INDENT - MARK_L, INDENT + STOCK + ind_mark * right_height_bc),
                          (INDENT, INDENT + STOCK + ind_mark * right_height_bc))
                draw.line((INDENT - MARK_L, INDENT - STOCK + ind_mark * right_height_bc),
                          (INDENT, INDENT - STOCK + ind_mark * right_height_bc))

                draw.line((INDENT + MARK_L + count_hor * right_width_bc, INDENT + STOCK + ind_mark * right_height_bc),
                          (INDENT + count_hor * right_width_bc, INDENT + STOCK + ind_mark * right_height_bc))
                draw.line((INDENT + MARK_L + count_hor * right_width_bc, INDENT - STOCK + ind_mark * right_height_bc),
                          (INDENT + count_hor * right_width_bc, INDENT - STOCK + ind_mark * right_height_bc))

        draw(page)


def draw_business_cards(width, height, width_bc, height_bc, front_files, back_files) -> BytesIO:
    """Функция для создания листов и вставки на них визиток оптимальным образом"""

    # Переводим размеры листа и визиток в пиксели
    width = mm_to_px(width)
    height = mm_to_px(height)
    width_bc = mm_to_px(width_bc + INIT_STOCK * 2)
    height_bc = mm_to_px(height_bc + INIT_STOCK * 2)

    # Проверка на оптимальное расположение при повороте визитки
    need_turn = 1
    right_width_bc = height_bc
    right_height_bc = width_bc
    count_ver, count_hor = (height - INDENT * 2) // width_bc, (width - INDENT * 2) // height_bc
    if (height - INDENT * 2) // height_bc * ((width - INDENT * 2) // width_bc) > count_ver * count_hor:
        need_turn = 0
        right_width_bc, right_height_bc = right_height_bc, right_width_bc
        count_ver, count_hor = (height - INDENT * 2) // height_bc, ((width - INDENT * 2) // width_bc)

    # Создаем объект BytesIO
    output_stream = BytesIO()

    # Создаем пустой лист
    with Image() as output_file:
        # Вставляем изображения на лист
        for front_file, back_file in zip(front_files, back_files):
            # Возвращаемся к началу потока
            front_file.stream.seek(0)
            back_file.stream.seek(0)

            with Image(file=front_file.stream) as fbc, \
                    Image(width=width, height=height, background=Color("white")) as page:
                # Устанавливаем разрешение изображений
                fbc.resolution = (DPI, DPI)
                page.resolution = (DPI, DPI)

                fbc.resize(width_bc, height_bc)

                if need_turn:
                    fbc.rotate(90)

                for y in range(count_ver):
                    for x in range(count_hor):
                        page.composite(fbc, left=INDENT + x * right_width_bc, top=INDENT + y * right_height_bc)
                # Делаем маркеры на лицевой стороне
                draw_mark(count_hor, count_ver, right_width_bc, right_height_bc, page)
                # Сохраняем лист с лицевой стороной
                output_file.sequence.append(page)

            with Image(file=back_file.stream) as bbc, \
                    Image(width=width, height=height, background=Color("white")) as page2:
                # Устанавливаем разрешение изображений
                bbc.resolution = (DPI, DPI)
                page2.resolution = (DPI, DPI)

                bbc.resize(width_bc, height_bc)

                if need_turn:
                    bbc.rotate(-90)

                for y in range(count_ver):
                    for x in range(1, count_hor + 1):
                        page2.composite(bbc, left=width - INDENT - x * right_width_bc, top=INDENT + y * right_height_bc)
                # Сохраняем лист с оборотной стороной
                output_file.sequence.append(page2)
        # Устанавливаем формат выходного файла как PDF
        output_file.format = 'pdf'
        # Сохраняем результирующий PDF в объект BytesIO
        output_file.save(file=output_stream)
    # Сбрасываем указатель на начало потока
    output_stream.seek(0)

    return output_stream
