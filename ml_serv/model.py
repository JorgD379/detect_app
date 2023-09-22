import cv2
import supervision as sv
import torch
from transformers import DetrForObjectDetection, DetrImageProcessor

def init(path):
    # settings
    DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    CHECKPOINT = 'facebook/detr-resnet-50'
    CONFIDENCE_TRESHOLD = 0.5
    IOU_TRESHOLD = 0.8

    image_processor = DetrImageProcessor.from_pretrained(CHECKPOINT)
    model = DetrForObjectDetection.from_pretrained(path)
    return image_processor, model, DEVICE, CONFIDENCE_TRESHOLD


def detect(image_processor, model, DEVICE, CONFIDENCE_TRESHOLD, image):
    with torch.no_grad():
        # load image and predict
        image = cv2.imread('/content/24_10_03_38_878082-2023-09-09_35451.jpg')
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