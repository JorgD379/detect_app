from flask import Flask, request

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Получаем файл из запроса
        file = request.files['photo']

        if file:

            return "ok", 200
        else:
            return "Файл не найден", 400
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True)
