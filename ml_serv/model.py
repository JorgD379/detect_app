import cv2
import supervision as sv
import torch
import numpy as np
from transformers import DetrForObjectDetection, DetrImageProcessor
from flask import Flask, request, jsonify


def init(path):
    # settings
    DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    CHECKPOINT = 'facebook/detr-resnet-50'
    CONFIDENCE_TRESHOLD = 0.5
    IOU_TRESHOLD = 0.8

    image_processor = DetrImageProcessor.from_pretrained(CHECKPOINT)
    model = DetrForObjectDetection.from_pretrained(path)
    return (image_processor, model, DEVICE, CONFIDENCE_TRESHOLD)


def detect(model_params, image):
    with torch.no_grad():
        # load image and predict
        image_processor, model, DEVICE, CONFIDENCE_TRESHOLD = model_params
        inputs = image_processor(images=image, return_tensors='pt')
        outputs = model(**inputs)

        # post-process
        target_sizes = torch.tensor([image.shape[:2]]).to(DEVICE)
        results = image_processor.post_process_object_detection(
            outputs=outputs,
            threshold=CONFIDENCE_TRESHOLD,
            target_sizes=target_sizes
        )[0]

    # annotate
    detections = sv.Detections.from_transformers(transformers_results=results)
    # print(np.array(detections))
    return jsonify(detections)