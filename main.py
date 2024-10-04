import os
from flask import Flask, request, render_template, send_file
from src.utility import get_paper_size, allowed_file
from src.generate_pdf import draw_business_cards

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # Отправляем данные на сервер. Срабатывает при нажатии "Сгенерировать файл для печати"
        # Получаем информацию из полей формы
        size_w = (request.form['cust_size_w'])
        size_h = (request.form['cust_size_h'])
        if len(size_h) == 0 or len(size_w) == 0:
            paper_size = request.form['paper_size']
            size_w, size_h = get_paper_size(paper_size)
        else:
            size_w, size_h = int(size_w), int(size_h)

        card_width = int(request.form['card_width'])
        card_height = int(request.form['card_height'])

        for size in size_w, size_h, card_width, card_height:
            if size <= 0:
                raise ValueError('Визитки или лист не могут иметь неположительный размер')

        front_files = request.files.getlist('front_files')
        back_files = request.files.getlist('back_files')

        if len(front_files) != len(back_files):
            raise ValueError('Количество лицевых сторон визиток должно совпадать с количеством задних сторон')

        for file in front_files + back_files:
            filename = os.path.basename(file.filename)
            if not allowed_file(filename):
                raise ValueError('Ваш формат визитки не поддерживается сервисом. Можете попробовать изменить файл '
                                 'конфигурации, но нет гарантии в получении ожидаемого результата')

        # Генерируем поток с pdf файлом
        out_pdf = draw_business_cards(size_w, size_h, card_width, card_height, front_files, back_files)
        # Возвращаем пользователю pdf файл
        return send_file(out_pdf, as_attachment=True, download_name="output.pdf", mimetype='application/pdf')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
