import cv2
import numpy as np
from flask import Flask, request
import model as m
app = Flask(__name__)
model_params = None
import json

new_image = 1

# label_dict = {
#     "1": "СПО250.14.190",
#     "2": "СК50.02.01.411",
#     "3": "СК50.01.01.404",
#     "4": "СК30.01.01.03.403",
#     "5": "СК30.01.01.02.402",
#     "6": "СК20.01.01.02.402",
#     "7": "СК20.01.01.01.406",
#     "8": "СВП120.42.030",
#     "9": "СВП120.42.020",
#     "10": "СВП-120.00.060",
#     "11": "СВМ.37.060А",
#     "12": "СВМ.37.060",
#     "12": "ЗВТ86.103К-02",
#     "15": "SU160.00.404",
#     "16": "SU80.10.409A",
#     "17": "SU80.01.426",
#     "13": "CS150.01.427-01",
#     "14": "CS120.07.442",
#     "19": "CS120.01.413",
# }

label_dict = {
    "1": "СПО250.14.190",
    "2": "СК50.02.01.411",
    "3": "СВП120.42.030",
    "4": "СВП-120.00.060",
    "5": "СВМ.37.060А",
}

def preproc_res(res):
    return [str(l) for l in res]

@app.route('/api/ml', methods=['POST'])
def upload_file():
    global new_image
    try:
        # Получаем файл из запроса
        file = request.files['file']

        if file:
            #file.save(str(new_image) + ".jpg")
            #new_image = new_image + 1
            img_stream = file.read()

            nparr = np.frombuffer(img_stream, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            lbl, scr = m.detect(model_params, image)
            lbl = preproc_res(lbl)
            scr = preproc_res(scr)

            max_values = {}
            for key, value in zip(lbl, scr):
                if key not in max_values or value > max_values[key]:
                    max_values[key] = value
            lbl = list(max_values.keys())
            scr = list(max_values.values())
            res = {'labels': lbl, 'score': scr}
            json_object = json.dumps(res)
            return json_object, 200
        else:
            return "Файл не найден", 400
    except Exception as e:
        print(str(e))
        return str(e), 500


if __name__ == '__main__':
    model_params = m.init(f"app/mdl")
    app.run(debug=True, host="0.0.0.0")