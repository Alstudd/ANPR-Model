# python -m venv env: python virtual environment

from io import BytesIO
from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for, Response
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess

from db import db_init, db
from myModels import Img
import cv2
import easyocr
import base64
import random

app = Flask(__name__)

app.static_folder = 'static'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

save_dir = os.path.join('static', 'Saved')
os.makedirs(save_dir, exist_ok=True)

numberPlateCascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
minArea = 500
color = (255, 0, 255)

@app.route("/detect", methods=['GET', 'POST'])
def detect():
    if not request.method == "POST":
        return
    mainFile = request.files['video']
    if not mainFile:
        return 'No file uploaded!', 400
    mainFile.save(os.path.join(uploads_dir, secure_filename(mainFile.filename)))
    print(mainFile)

    # image to url
    with open(os.path.join(uploads_dir, secure_filename(mainFile.filename)), "rb") as image_file:
        image_data = image_file.read()
        base64_data = base64.b64encode(image_data).decode("utf-8")
        data_url = f"data:{mainFile.mimetype};base64,{base64_data}"
    
    numberPlateText = ""
    randNum = random.randint(1, 100)
    if "image" in str(mainFile.mimetype):
        img = cv2.imread(os.path.join(uploads_dir, secure_filename(mainFile.filename)))
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        numberPlates = numberPlateCascade.detectMultiScale(imgGray, 1.1, 4)
        for (x, y, w, h) in numberPlates:
            area = w*h
            if area > minArea:
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
                cv2.putText(img, f"Number Plate {numberPlateText}", (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
                imgROI = img[y:y+h, x:x+w]
        reader = easyocr.Reader(['en'])
        result = reader.readtext(imgROI)
        print(result)
        for tup in result:
            for i in tup:
                if isinstance(i, str):
                    numberPlateText = i
                    break
            break
        # numberPlateText = result[0][-2]
        print(numberPlateText)
        cv2.imwrite("static/Saved/"+secure_filename(mainFile.filename), imgROI)
    elif "video" in str(mainFile.mimetype):
        frameWidth = 320
        frameHeight = 280
        cap = cv2.VideoCapture(os.path.join(uploads_dir, secure_filename(mainFile.filename)))
        cap.set(3, frameWidth)
        cap.set(4, frameHeight)
        cap.set(10, 150)
        count = 0
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        fps = cap.get(cv2.CAP_PROP_FPS)
        # Video Writer
        # video_writer = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('P','I','M','1'), fps, (width, height))

        while True:
            success, img = cap.read()
            if not success:
                return "Unsuccessful", 400
            # video_writer.write(img)
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            numberPlates = numberPlateCascade.detectMultiScale(imgGray, 1.1, 4)
            for (x, y, w, h) in numberPlates:
                area = w*h
                if area > minArea:
                    cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(img, "Number Plate", (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
                    imgROI = img[y:y+h, x:x+w]
                    # cv2.imshow("ROI", imgROI)
            # cv2.imshow("Result", img)
            # if cv2.waitKey(1) & 0xFF == ord('s'):
            #     cv2.imwrite("Saved/NoPlate_"+str(count)+".jpg", imgROI)
            #     cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
            #     cv2.putText(img, "Image Saved", (150, 265), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 2)
            #     cv2.imshow("Result", img)
            #     cv2.waitKey(500)
            #     count += 1
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            if count == 20:
                reader = easyocr.Reader(['en'])
                result = reader.readtext(imgROI)
                print(result)
                for tup in result:
                    for i in tup:
                        if isinstance(i, str):
                            numberPlateText = i
                            # break
                    # break
                print(numberPlateText)
                cv2.imwrite("static/Saved/"+f"Result{randNum}"+".jpg", imgROI)
                break
            count += 1
        cap.release()
        # video_writer.release()
    else:
        return 'Not allowed!', 400
    
    # result_image_data = BytesIO(imgROI.read())
    # result_base64_data = base64.b64encode(image_data).decode("utf-8")
    # result_data_url = f"data:{mainFile.mimetype};base64,{result_base64_data}"
    
    fileName = secure_filename(mainFile.filename)
    mimeType = mainFile.mimetype
    if not fileName or not mimeType:
        return 'Bad upload!', 400

    uploadedFile = Img(originalImgData=image_data, name=fileName, mimetype=mimeType, originalImgURL=data_url)
    db.session.add(uploadedFile)
    db.session.commit()

    if "video" in str(mainFile.mimetype):
        return [f"Result{randNum}.jpg", numberPlateText]
    return [fileName, numberPlateText]

@app.route("/")
def hello_world():
    return render_template('index.html')


def generate_frames(camera):
    camera.set(10, 150)
    while True:
            
        ## read the camera frame
        success,img=camera.read()   
        if not success:
            break
        else:
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            numberPlates = numberPlateCascade.detectMultiScale(imgGray, 1.1, 4)
            for (x, y, w, h) in numberPlates:
                area = w*h
                if area > minArea:
                    cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(img, "Number Plate", (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
                    # imgROI = img[y:y+h, x:x+w]
                    
            ret,buffer=cv2.imencode('.jpg',img)
            img=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
        
# def generate_frames_no_plate():
#     while True:
            
#         ## read the camera frame
#         imgROI = ""
#         success,img=camera.read()   
#         if not success:
#             break
#         else:
#             imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             numberPlates = numberPlateCascade.detectMultiScale(imgGray, 1.1, 4)
#             for (x, y, w, h) in numberPlates:
#                 area = w*h
#                 if area > minArea:
#                     cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
#                     cv2.putText(img, "Number Plate", (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
#                     imgROI = img[y:y+h, x:x+w]
                    
#             ret,buffer=cv2.imencode('.jpg',img)
#             imgROI=buffer.tobytes()

        # yield(b'--frame\r\n'
        #            b'Content-Type: image/jpeg\r\n\r\n' + imgROI + b'\r\n')

@app.route("/opencam", methods=['GET', 'POST'])
def opencam():
    camera = cv2.VideoCapture(0)
    return Response(generate_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/webcam", methods=['GET', 'POST'])
def webcam():
    return render_template("webcam.html")

@app.route("/realTimeVideo", methods=['GET', 'POST'])
def realTimeVideo():
    camera = cv2.VideoCapture("static/video2.mp4")
    return Response(generate_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/videocam", methods=['GET', 'POST'])
def videocam():
    return render_template("realTimeVideoCam.html")

@app.route('/<int:id>')
def get_file(id):
    uploadedFile = Img.query.filter_by(id=id).first()
    if not uploadedFile:
        return 'File Not Found!', 404
    return Response(uploadedFile.img, mimetype=uploadedFile.mimetype)

@app.route("/display/<filename>")
def display_file(filename):
    uploadedFile = Img.query.filter_by(name=filename).first()
    if not uploadedFile:
        return 'File Not Found!', 404
    return send_file(BytesIO(uploadedFile.img), mimetype=uploadedFile.mimetype, download_name=uploadedFile.name)

@app.route('/download/<filename>')
def download_file(filename):
    uploadedFile = Img.query.filter_by(name=filename).first()
    if not uploadedFile:
        return 'File Not Found!', 404 
    return send_file(BytesIO(uploadedFile.img), mimetype=uploadedFile.mimetype, download_name=uploadedFile.name, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)