from flask import Flask, request
import model as m
app = Flask(__name__)


@app.route('/api/ml', methods=['POST'])
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
    model_params = m.init("model_path")
    app.run(debug=True)