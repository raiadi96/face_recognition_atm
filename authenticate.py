import cv2
import numpy as np
import dlib
from imutils import face_utils
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import time
from random import randint
import os

# starting camera
# 0 is the web camera source
# add any link in quotes for playing videos
def authen():
    cap = cv2.VideoCapture(0)

    # initiating dlib detector for frontal face_detection

    dlib_detector = dlib.get_frontal_face_detector()

    # using 5 point facial landmark detector for extracting face, eyes, mouth and nose
    predictor = dlib.shape_predictor('shape_predictor_5_face_landmarks.dat')
    fa = FaceAligner(predictor, desiredFaceWidth=256)

    # using haar cascade to detect the outline of a face
    detect_face = cv2.CascadeClassifier(cv2.data.haarcascades + r"haarcascade_frontalface_default.xml")
    while (True):
        # reading from camera
        ret, frame = cap.read()
        # segmentation begins here

        # single channel image for faster processing
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faceAligned = gray_frame
        dup_frame = frame.copy()
        # building scaled outline of face and then detecting all the rectangles formed. A rectangle will dentoe the outline of the face.
        faces = detect_face.detectMultiScale(gray_frame, scaleFactor=4)
        rects = dlib_detector(gray_frame, 0)
        if len(rects) > 0:
            text = "{} face(s) found".format(len(rects))
            cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)
        for i, rect in enumerate(rects):
            # compute the bounding box of the face and draw it on the
            # frame

            (bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
            cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH),
                          (0, 255, 0), 1)
            dup_frame = dup_frame[bY:bY + bW, bX:bX + bW]
            # cropped_image = frame[bX:bX+5*bH,bY:bY+5*bW]
            # cv2.namedWindow("cropped image",2)
            # cv2.imshow("cropped image",cropped_image)

            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray_frame, rect)
            shape = face_utils.shape_to_np(shape)

            if cv2.waitKey(1) & 0xFF == ord('c'):


                #faceAligned = fa.align(dup_frame, gray_frame, rect)
                import recognition_system

                cv2.destroyAllWindows()
                name =recognition_system.start(dup_frame)

                return name


            # loop over the (x, y)-coordinates for the facial landmarks
            # and draw each of them
            for (i, (x, y)) in enumerate(shape):
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
                cv2.putText(frame, str(i + 1), (x - 10, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), color=[125, 255, 187], thickness=2)

            # cv2.putText(frame,text="I am awesome",org=(x, h), fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0, color = (255, 255, 255), lineType=cv2.LINE_AA)

        cv2.imshow("vid", frame)

        # cv2.imshow("s",faceAligned)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    cap.release()

    cv2.destroyAllWindows()