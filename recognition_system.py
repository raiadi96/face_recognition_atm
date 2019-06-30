import face_recognition
import argparse
import cv2
import pickle

#argument

'''ap = argparse.ArgumentParser()
ap.add_argument("-e","--encodings",required=True,help="Path to the encoded file")
ap.add_argument("-i","--image",required=True,help="Path to the image")
ap.add_argument("-d","--method",type=str,default="cnn",help="face detection model to be used")
args = vars(ap.parse_args())'''

def start(im):
#load all the known faces and encodings
    print("**Loading Encodings...**")
    file = open("data.pickle","rb").read()
    data = pickle.loads(file)

    print(data["encodings"])

    #load the input image
    image = im
    image  = cv2.resize(image,(100,100))
    #image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

    #detect coordinates of the bounding box correspinding to each face in input image.
    print("**Recognising faces..**")
    boxes = face_recognition.face_locations(image,model="hog")
    encodings = face_recognition.face_encodings(image,boxes)
    names = []
    #loop over the facial encodings
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"],encoding)
        name = "Unknown"

        if True in matches:
            matchedIdxs = [i for (i,b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name,0)+1

            name = max(counts,key=counts.get)

        names.append(name)

    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 255, 0), 2)
    return name
    # show the output image
