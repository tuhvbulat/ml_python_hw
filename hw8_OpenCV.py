import cv2

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
WIDTH = 775
HEIGHT = 600
COLOR = (0,165,255)

def detectLargestFace():
    capture = cv2.VideoCapture(0)
    cv2.namedWindow("result-image", cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow("result-image",400,100)
    cv2.startWindowThread()
    rectangleColor = COLOR

    try:
        while True:
            rc,fullSizeBaseImage = capture.read()
            baseImage = cv2.resize( fullSizeBaseImage, ( 320, 240))
            pressedKey = cv2.waitKey(2)

            if pressedKey == ord('Q'):
                cv2.destroyAllWindows()
                exit(0)

            resultImage = baseImage.copy()
            gray = cv2.cvtColor(baseImage, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.3, 5)

            maxArea = 0
            x = 0
            y = 0
            w = 0
            h = 0

            for (_x,_y,_w,_h) in faces:
                if  _w*_h > maxArea:
                    x = _x
                    y = _y
                    w = _w
                    h = _h
                    maxArea = w*h
            
            if maxArea > 0 :
                cv2.rectangle(resultImage, (x-10, y-20), (x + w+10 , y + h+20), rectangleColor, 2)

            largeResult = cv2.resize(resultImage,(WIDTH,HEIGHT))
            cv2.imshow("result-image", largeResult)
    except KeyboardInterrupt as e:
        cv2.destroyAllWindows()
        exit(0)


if __name__ == '__main__':
    detectLargestFace()
