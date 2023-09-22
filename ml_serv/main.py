import cv2
import numpy as np
from flask import Flask, request, jsonify
import model as m
app = Flask(__name__)
model_params = None

@app.route('/api/ml', methods=['POST'])
def upload_file():
    try:
        # Получаем файл из запроса
        file = request.files['photo']

        if file:
            img_stream = file.read()
            nparr = np.frombuffer(img_stream, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            res = m.detect(model_params, image)
            print(res)
            return res, 200
        else:
            return "Файл не найден", 400
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    model_params = m.init("mdl")
    app.run(debug=True)