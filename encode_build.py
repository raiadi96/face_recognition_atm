from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

#creating argument parsing
'''ap = argparse.ArgumentParser()
ap.add_argument("-i","--dataset",required=True,help="Path of the dataset.(Compulsory)")
ap.add_argument("-e","--encodings",required=True,help="path to serialized db")
ap.add_argument("-d","--detection-method",type=str,default="cnn",help="hog or cnn")
args = vars(ap.parse_args())'''

#getting all image paths
def run_encode(path):

    image_path = list(paths.list_images(path))

    knownEncodings =[]
    knownNames = []

    for (i,imagePath) in enumerate(image_path):
        print("**Image {0} of {1}**".format(i+1,len(image_path)))
        name = imagePath.split(os.path.sep)[-2]
        name = name.split("/")[-1]
        print(name)
        image = cv2.imread(imagePath)

        image  = cv2.resize(image,(100,100))
        rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb,model="hog")

        encodings = face_recognition.face_encodings(rgb,boxes)

        for encoding in encodings:
            print("entering this")
            knownEncodings.append(encoding)
            knownNames.append(name)

    if os.path.exists("data.pickle"):
        pickle_data = open("data.pickle","rb")
        dict = pickle.load(pickle_data)
        encoding = dict['encodings']

        encoding = encoding + knownEncodings

        names = dict['names']
        print("names",names)
        print("known",knownNames)
        names = names+knownNames

        print(names)
        print(len(encoding))

        pickle_data.close()
        #encoding.append(knownEncodings)
        #names.append(knownNames)
        pickle_data= open("data.pickle","wb")
        data = {"encodings": encoding, "names": names}
        pickle_data.write(pickle.dumps(data))
        pickle_data.close()
        print("completed")

    else:

        print("**Serializing Encoding...**")
        data = {"encodings":knownEncodings,"names":knownNames}

        f = open("data.pickle","wb")
        f.write(pickle.dumps(data))
        f.close()





run_encode("C:/Users/rai_a/PycharmProjects/final_year_face_recogn/aligned_image_data/aditya")