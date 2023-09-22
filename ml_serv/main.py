import cv2
import numpy as np
from flask import Flask, request, jsonify
import model as m
app = Flask(__name__)
model_params = None
import json

def preproc_res(res):
    return [str(l) for l in res]

@app.route('/api/ml', methods=['POST'])
def upload_file():
    try:
        # Получаем файл из запроса
        file = request.files['file']

        if file:
            img_stream = file.read()
            nparr = np.frombuffer(img_stream, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            lbl, scr = m.detect(model_params, image)
            lbl = preproc_res(lbl)
            scr = preproc_res(scr)
            res = {'labels': lbl, 'score': scr}
            json_object = json.dumps(res)
            return json_object, 200
        else:
            return "Файл не найден", 400
    except Exception as e:
        print(str(e))
        return str(e), 500


if __name__ == '__main__':
    model_params = m.init("mdl")
    app.run(debug=True, host="192.168.66.49")