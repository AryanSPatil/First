# Threading is used for simultaneous processing.
import threading
# Importing libraries like OpenCV and deepface.
import cv2
from deepface import DeepFace
#Sets which camera captures the video, in this case its camera 0,
#which means the first camera it detects
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#Provides Frame size for window
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#Counter to check frames in interval of 30(to reduce load)
counter = 0
#Boolean to facematch
face_match = False
#Providing a reference image
reference_img = cv2.imread("IMG_20210521_142909.jpg")
#Deepface verifies the frame for the image
def check_face(frame):
    global face_match
    try:
        if DeepFace.verify(frame, reference_img.copy())['verified']:
            face_match = True

        else:
            face_match = False
    except ValueError:
        face_match = False
#Reading the frame and displaying text on screen
while True:
    ret, frame = cap.read()

    if ret :
        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            except ValueError:
                pass
        
        counter += 1

        if face_match :

            cv2.putText(frame,"MATCH!!", (20, 450),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0,255,0), 3)

        else :

            cv2.putText(frame,"NO MATCH!!", (20, 450),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0,0,255), 3)
        cv2.imshow("Video", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
#Clears all windows
cv2.destroyAllWindows()