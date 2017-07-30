from flask import Flask, render_template, Response
import cv2
import sys


faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#faceCascade = cv2.CascadeClassifier("hand1.xml")

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen_from_cam():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            area = w*h
            if area > 100000:
                print("big")
            else:
                print("small")
        cv2.imwrite("test.jpg", frame)
        f = open("test.jpg", 'rb').read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + f + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_from_cam(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
