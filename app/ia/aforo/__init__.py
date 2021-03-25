"""
Editor: Ahan M R
Date: 18-06-2018
Python 3.6.0
"""

# PS1 CROWD DETECTION IN THE SITUATION
'''
From imageAI API, we import Object detection and use it to detect the object classes in the image
'''

from imageai.Detection import ObjectDetection
import os

# os.getcwd gets the current working directory of the image
execution_path = os.getcwd()

detection = ObjectDetection()
detection.setModelTypeAsRetinaNet()
detection.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
detection.loadModel()
detections = detection.detectObjectsFromImage(input_image=os.path.join(execution_path, "personas.jpeg"),
                                              output_image_path=os.path.join(execution_path, "imagenew.jpg"))

for eachObject in detections:
    print(eachObject["name"] + " : " + eachObject["percentage_probability"])
