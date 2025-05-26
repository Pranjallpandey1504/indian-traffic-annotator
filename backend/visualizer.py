import cv2
import os
import xml.etree.ElementTree as ET

IMAGE_DIR = "../images/"
ANNOTATION_DIR = "../annotations/"

# Resize parameters
DISPLAY_WIDTH = 800  # you can tweak this
DISPLAY_HEIGHT = 600

# Loop through all XML files
for file in os.listdir(ANNOTATION_DIR):
    if file.endswith(".xml"):
        xml_path = os.path.join(ANNOTATION_DIR, file)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        filename = root.find("filename").text
        img_path = os.path.join(IMAGE_DIR, filename)

        # Load the image
        image = cv2.imread(img_path)
        if image is None:
            continue

        # Draw each object
        for obj in root.findall("object"):
            name = obj.find("name").text
            bndbox = obj.find("bndbox")
            x1, y1 = int(bndbox.find("xmin").text), int(bndbox.find("ymin").text)
            x2, y2 = int(bndbox.find("xmax").text), int(bndbox.find("ymax").text)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        # Resize image for display
        resized_image = cv2.resize(image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

        cv2.imshow("Annotated Image", resized_image)
        cv2.waitKey(0)

cv2.destroyAllWindows()
