import os
from google.cloud import vision
import io

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + "/flaskblog/gallery/key.json"

def detect_labels(path):
    """Detects labels in the file."""
    labels_str = ""
    try:
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.label_detection(image=image)
        labels = response.label_annotations
        print('Labels:')

        for label in labels:
            if label.score > 0.9:
                print(label.description, label.score)
                labels_str = labels_str + label.description + ", "
    except:
        print('Could not retrieve Google Vision labels.')

    return labels_str
