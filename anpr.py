import cv2

numberPlateCascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
minArea = 500
color = (255, 0, 255)
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture("video1.mp4")
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)
count = 0

while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = numberPlateCascade.detectMultiScale(imgGray, 1.1, 4)
    for (x, y, w, h) in numberPlates:
        area = w*h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
            cv2.putText(img, "Number Plate", (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
            imgROI = img[y:y+h, x:x+w]
            cv2.imshow("ROI", imgROI)
    cv2.imshow("Result", img)
    # if cv2.waitKey(1) & 0xFF == ord('s'):
    #     cv2.imwrite("Saved/NoPlate_"+str(count)+".jpg", imgROI)
    #     cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
    #     cv2.putText(img, "Image Saved", (150, 265), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 2)
    #     cv2.imshow("Result", img)
    #     cv2.waitKey(500)
    #     count += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if count == 20:
        cv2.imwrite("Saved/NoPlate_"+str(count)+".jpg", imgROI)
        break
    count += 1
    
    

# img = cv2.imread("p1.jpg")
# imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# numberPlates = numberPlateCascade.detectMultiScale(imgGray, 1.1, 4)
# for (x, y, w, h) in numberPlates:
#     area = w*h
#     if area > minArea:
#         cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
#         cv2.putText(img, "Number Plate", (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
#         imgROI = img[y:y+h, x:x+w]
# cv2.imwrite("Saved/NoPlate_"+"Result"+".jpg", imgROI)