import cv2
import numpy as np
from flask import Flask, request
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

            # Отображаем фотографию с помощью OpenCV
            cv2.imshow('Received Image', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return "ok", 200
        else:
            return "Файл не найден", 400
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    model_params = m.init("mdl")
    app.run(debug=True)