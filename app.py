import numpy as np
import cv2
import streamlit as st
import tempfile
from streamlit_webrtc import webrtc_streamer

NMS_THRESHOLD = 0.3
MIN_CONFIDENCE = 0.2

labelsPath = "coco.names"
LABELS = open(labelsPath).read().strip().split("\n")

weights_path = "yolov4-tiny.weights"
config_path = "yolov4-tiny.cfg"


writer = None

stframe = st.empty()
SCALE_OUTPUT = 1


def pedestrian_detection(image, model, layer_name, personidz=0):

    (H, W) = image.shape[:2]
    results = []

    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    model.setInput(blob)
    layerOutputs = model.forward(layer_name)

    boxes = []
    centroids = []
    confidences = []

    for output in layerOutputs:
        for detection in output:

            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if classID == personidz and confidence > MIN_CONFIDENCE:

                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                centroids.append((centerX, centerY))
                confidences.append(float(confidence))
    # apply non-maxima suppression to suppress weak, overlapping
    # bounding boxes
    idzs = cv2.dnn.NMSBoxes(boxes, confidences, MIN_CONFIDENCE, NMS_THRESHOLD)
    # ensure at least one detection exists
    if len(idzs) > 0:
        # loop over the indexes we are keeping
        for i in idzs.flatten():
            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            # update our results list to consist of the person
            # prediction probability, bounding box coordinates,
            # and the centroid
            res = (confidences[i], (x, y, x + w, y + h), centroids[i])
            results.append(res)
    # return the list of results
    return results


model = cv2.dnn.readNetFromDarknet(config_path, weights_path)
layer_name = model.getLayerNames()
layer_name = [layer_name[i - 1] for i in model.getUnconnectedOutLayers()]
try:
    st.title("Human detection with YOLOV4")
    st.subheader("Choose appropriate Method")

    method = st.selectbox('Choose the method', [
                          'CAMERA', 'VIDEO FILE'], index=0)

    if method == 'CAMERA':
        #cap = cv2.VideoCapture(0)
        webrtc_streamer(key="key")
    elif method == 'VIDEO FILE':
        video_file_buffer = st.file_uploader(
            "Upload a video", type=["mp4", "mov", 'avi', 'asf', 'm4v'])
        if video_file_buffer is not None:

            tffile = tempfile.NamedTemporaryFile(delete=False)
            tffile.write(video_file_buffer.read())
            cap = cv2.VideoCapture(tffile.name)

            while cap.isOpened():
                grabbed, image = cap.read()
                input_video_frame_height, input_video_frame_width = image.shape[:2]
                target_frame_height = int(
                    input_video_frame_height * SCALE_OUTPUT)
                target_frame_width = int(
                    input_video_frame_width * SCALE_OUTPUT)

                if not grabbed:
                    cap.release()
                    break
                #image = to_rgb(convert_result_to_image(image))
                resize_image = cv2.resize(src=image, dsize=(
                    target_frame_width, target_frame_height))
                #resize_image = imutils.resize(image, width = target_frame_width )
                results = pedestrian_detection(resize_image, model, layer_name,
                                               personidz=LABELS.index("person"))
                # st.write("pass")
                for res in results:
                    cv2.rectangle(resize_image, (res[1][0], res[1][1]),
                                  (res[1][2], res[1][3]), (0, 255, 0), 2)
                cv2.putText(resize_image, f'Total Persons = {len(results) - 1}',
                            (80, 80), cv2.FONT_HERSHEY_DUPLEX, 2.5, (0, 255, 0), 4)

                #stacked_frame = np.vstack((resize_image, image))
                stacked_frame = np.array(resize_image)
                #stacked_frame = Image.fromarray(resize_image)
                stframe.image(stacked_frame, channels='BGR',
                              use_column_width=True)

                key = cv2.waitKey(0)
                if key == 27:
                    break

            cap.release()
            # out.release()
            cv2.destroyAllWindows()
            #st.success('Video is processed')
            st.stop()
except AttributeError:
    pass
