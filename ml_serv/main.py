import base64
from io import BytesIO

import cv2
import numpy as np
from flask import Flask, request, jsonify
import model as m
app = Flask(__name__)
model_params = None
import json
from PIL import Image, ImageDraw

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

titles_dict = {'code':"Деталь",
               'name':"Имя",
               'weight':"Масса",
               'roughness':"Шероховатость",
               'surface':"Покрытие",
               'extra':"Дополнительно"}

label_dict = {
    "1": {"code":"СПО250.14.190",
          "name":"Фланец",
          "weight":"0.23",
          "roughness":"Ra 25"},
    "2": {"code":"СК50.02.01.411",
          "name":"Кронштейн",
          "weight":"0.4",
          "roughness": "Ra 12.5",
          "surface": "Покрытие поверхности Грунт-Эмаль RAL 7025",
          "extra": "Гнуть по линии гравировки"},
    "3": {"code":"СВП120.42.030",
          "name":"Шкив",
          "weight":"4.5",
          "surface": "Покрытие поверхности Грунт I-III группа по ИСО 12944, Эмаль I-III группа по ИСО 12944, RAL 7024 (цв. графитовый серый)",
          "extra": "Сварная конструкция I класса по Ост 23.2.429-80"},
    "4": {"code":"СВМ.37.060А",
          "name":"Кронштейн для крепления датчика температуры",
          "weight":"0.237",
          "surface": "Покрытие поверхностей: Грунт I-III группа по ИСО 12944, Эмаль I-III группа по ИСО 12944, RAL 7024 (цв. графитовый серый). РЕЗЬБОВУЮ ПОВЕРХНОСТЬ НЕ ПОКРЫВАТЬ!",
          "extra": "Сварная конструкция II класса по Ост 23.2.429-80\n"},
    "5": {"code":"SU160.00.404",
          "name":"Кронштейн",
          "weight":"0.638",
          "roughness": "Ra 25",
          "surface": "Покрытие поверхностей: Грунт I-III группа по ИСО 12944, Эмаль I-III группа по ИСО 12944, RAL 7024 (цв. графитовый серый)"},
    "6": {"code":"SU80.10.409A",
          "name":"Ушка",
          "weight":"1.299",
          "roughness": "Ra 12.5",
          "surface": "Покрытие поверхностей: Грунт I-III группа по ИСО 12944, Эмаль I-III группа по ИСО 12944, RAL 7024 (цв. графитовый серый)"},
    "7": {"code": "GS120.01.413",
          "name": "Опора актуатора",
          "weight": "1.6",
          "roughness": "Ra 12.5",
          "surface": "Покрытие поверхностей: Грунт I-III группа по ИСО 12944, Эмаль I-III группа по ИСО 12944, RAL 7024 (цв. графитовый серый)"},
    "8": {"code": "GS150.01.427-01",
          "name": "Стенка",
          "weight": "2.8",
          "roughness": "Ra 12.5",
          "surface": "Покрытие поверхностей: Грунт I-III группа по ИСО 12944, Эмаль I-III группа по ИСО 12944, RAL 7024 (цв. графитовый серый)"},
    "9": {"code": "СВП-120.00.060",
          "name": "Ручка",
          "weight": "1.05",
          "roughness": "Ra 25",
          "extra": "Деталь изг. на комплексе лазерной резки"},
    "10": {"code": "ЗВТ86.103К-02",
          "name": "Шкив",
          "weight": "см.табл.",
          "roughness": "Ra 12.5",
          "surface": "Покрытие поверхностей, кроме резьбовых и посадочных: Грунт I-III группа по ИСО 12944, Эмаль I-III группа по ИСО 12944, RAL 7024 (цв. графитовый серый)"},
}

def desc_to_str(desc, l):
    res = "Метка: " + l + "\n"
    for title in desc:
        res+= titles_dict[title] + ": " + desc[title] + "\n"
    return res

def preproc_res(inp):
    res_bbx = []
    for bbx in inp[0]:
        res_bbx.append([str(l) for l in bbx])
    res_lbl = [str(l) for l in inp[1]]
    res_scr = [str(l) for l in inp[2]]
    return res_bbx, res_lbl, res_scr


def add_rectangle_to_image(image, rects):
    img = Image.open(image)
    draw = ImageDraw.Draw(img)
    for rect in rects:
        x1, y1, x2, y2 = rect
        draw.rectangle([x1, y1, x2, y2], outline="red", width=10)

    img_byte_array = BytesIO()
    img.save(img_byte_array, format="PNG")
    img_base64 = base64.b64encode(img_byte_array.getvalue()).decode('utf-8')
    return img_base64

@app.route('/api/ml', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']

        if file:
            img_stream = file.read()
            nparr = np.frombuffer(img_stream, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            bbx, lbl, scr = m.detect(model_params, image)
            processed_image_data = add_rectangle_to_image(file, bbx)
            bbx, lbl, scr = preproc_res((bbx, lbl, scr))

            uniq = []
            for l in lbl:
                desc = label_dict[l]
                tmp = desc_to_str(desc, l)
                if tmp not in uniq:
                    uniq.append(tmp)

            # Отправьте изображение и данные в формате JSON
            res = {'labels': lbl, 'description': uniq, 'image': processed_image_data}
            json_object = jsonify(res)
            return json_object, 200
        else:
            return "Файл не найден", 400
    except Exception as e:
        print(str(e))
        return str(e), 500


if __name__ == '__main__':
    model_params = m.init(f"app/mdl")
    app.run(debug=True, host="0.0.0.0")