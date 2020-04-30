from imageai.Detection.Custom import CustomObjectDetection
import os
def path(image):
	img = image
	detector = CustomObjectDetection()
	detector.setModelTypeAsYOLOv3()
	detector.setModelPath("detection_model.h5")
	detector.setJsonPath("detection_config.json")
	detector.loadModel()
	detector.detectObjectsFromImage(input_image=img, output_image_path="mask-detected.jpg",display_percentage_probability=False)


'''
for detection in detections:
    print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])
'''