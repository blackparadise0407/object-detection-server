import sys
import time
import getopt
import os
import numpy as np
import cv2
OUTPUT_PATH = "D:\playground\ml\dogbreeds\server\public\output"


def main(argv):
    argument = ''
    usage = 'usage: detectNode.py -p <path/to/image>'
    # parse incoming arguments
    try:
        opts, args = getopt.getopt(argv, "hp:", ["path="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-p", "--path"):
            argument = arg
    # use the argument
    net = cv2.dnn.readNet(
        'D:\playground\ml\dogbreeds\server\detect\yolov3_training_dogbreeds_30000.weights', 'D:\playground\ml\dogbreeds\server\detect\yolov3_dogbreeds_testing.cfg')
    classes = []

    with open("D:\playground\ml\dogbreeds\server\detect\classes_dogbreeds.txt", "r") as f:
        classes = f.read().splitlines()

    font_scale = 1.5
    rectangle_bgr = (255, 255, 255)
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(100, 3))

    imgInput = cv2.imread(argument)
    img = cv2.resize(imgInput, (600, 480))
    height, width, channels = img.shape
    blob = cv2.dnn.blobFromImage(
        img, 1/255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)
    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)
    output_label = ""
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            tempW = round(w*0.75)
            tempH = round(h/8)
            halfY = round(y+tempH)
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = colors[i]
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
            text = label + " " + confidence
            (text_width, text_height) = cv2.getTextSize(
                text, font, fontScale=font_scale, thickness=1)[0]
            text_offset_x = x
            text_offset_y = y+h
            box_coords = ((text_offset_x, text_offset_y), (text_offset_x +
                                                           text_width + 2, text_offset_y - text_height - 2))
            cv2.rectangle(
                img, box_coords[0], box_coords[1], color, cv2.FILLED)
            cv2.putText(img, text, (text_offset_x, text_offset_y),
                        font, fontScale=font_scale, color=(0, 0, 0), thickness=1)
            output_label = text
    head, tail = os.path.split(argument)
    fileName = "out_"+tail
    print(fileName, output_label)
    cv2.imwrite(os.path.join(OUTPUT_PATH, fileName), img)
    location = "D:\\playground\\ml\\dogbreeds\\server\\public\\uploads"
    removePath = os.path.join(location, argument)
    os.remove(removePath)
    cv2.destroyAllWindows()


# MAIN
if __name__ == "__main__":
    main(sys.argv[1:])
