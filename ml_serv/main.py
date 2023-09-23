import cv2
import numpy as np
from flask import Flask, request
import model as m
app = Flask(__name__)
model_params = None
import json

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
}

extra_info = {
    "СПО250.14.190": {"name":"Фланец", "weight":"0.23"},
    "СК50.02.01.411": {"name":"Кронштейн", "weight":"0.4", "extra": "1) Покрытие поверхности Грунт-Эмаль RAL 7025\n2) Гнуть по линии гравировки."},
    "СВП120.42.030": {"name":"Шкив", "weight":"4.5", "extra": "1) Покрытие поверхности Грунт I - III группа по ИСО 12944, Эмаль I - III группа\n2) Сварная конструкция I класса по ОСТ 23.24.429-80."},
}

def preproc_res(inp):
    res_bbx = []
    for bbx in inp[0]:
        res_bbx.append([str(l) for l in bbx])
    res_lbl = [str(l) for l in inp[1]]
    res_scr = [str(l) for l in inp[2]]
    return res_bbx, res_lbl, res_scr

# def del_duplicates(inp):
#     bbxs, lbls, scrs = inp
#     for i in range(len(bbxs)):
#         for j in range(i+1, len(bbxs)):
#             R = [max(bbxs[i][0],bbxs[j][0]), max(bbxs[i][1],bbxs[j][1]), min(bbxs[i][2],bbxs[j][2]), min(bbxs[i][3],bbxs[j][3])]
#             if((R[0]+R[2])/2 > bbxs[i][0] and (R[0]+R[2])/2 < bbxs[i][2])
#             print(R)
#             break

@app.route('/api/ml', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']

        if file:
            img_stream = file.read()

            nparr = np.frombuffer(img_stream, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            bbx, lbl, scr = m.detect(model_params, image)
            print(bbx, lbl, scr)

            # del_duplicates((bbx, lbl, scr))

            bbx, lbl, scr = preproc_res((bbx, lbl, scr))
            res = {'bboxes': bbx, 'labels': lbl, 'score': scr}
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