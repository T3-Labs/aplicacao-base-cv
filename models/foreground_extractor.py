from turtle import right, width
import cv2
import numpy

class StaticForegroundExtractor:
    def __init__(self, backgroundModelFilePath = "models/bg_model/bg.png", mmpx = 2.96): #2.1428 #NOTE 2.96):
        self._background_model = cv2.imread(backgroundModelFilePath)
        self._morph_operator = cv2.getStructuringElement(cv2.MORPH_RECT,(3,1))
        self._mmpx = mmpx

    def extract_foreground(self, img):
        diff = cv2.subtract(img, self._background_model)
        diff = cv2.GaussianBlur(diff, (3,3), 1.8)

        maxDiff = numpy.amax(diff, axis=2)
        ret, thr = cv2.threshold(maxDiff, 127, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)

        foreground = cv2.morphologyEx(thr, cv2.MORPH_ERODE, self._morph_operator)
        
        return foreground
    
    def _get_shape_from_foreground_roi(self, fg, roiRect):

        minX = max(0,roiRect[0])
        minY = max(0,roiRect[1])

        maxX = min(fg.shape[1],roiRect[0]+roiRect[2])
        maxY = min(fg.shape[0],roiRect[1]+roiRect[3])

        roi = fg[minY:maxY, minX:maxX]
        contours, hierarchy = cv2.findContours(roi,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        biggestShape = 0
        maxSize = 0
        for contour in contours:
            if( contour.shape[0] > maxSize ):
                biggestShape = contour
                maxSize = contour.shape[0]

        biggestShape[:,:,0] += roiRect[0]
        biggestShape[:,:,1] += roiRect[1]
        
        return biggestShape

    def get_measurements_from_roi(self, fg, roiList):
        measurements = []
        for roi in roiList:
            shape = self._get_shape_from_foreground_roi(fg, roi)
            minArea = cv2.minAreaRect(shape)
            centerWH, sizeWH, angle = minArea
            #box = cv2.boxPoints(minArea) NOTE Arestas
            width, height = sizeWH
            measurements.append((width*self._mmpx, height*self._mmpx))
        return measurements

    @staticmethod
    def convertToVertices(box)->numpy.array:
        left_point_x = numpy.min(box[:, 0])
        right_point_x = numpy.max(box[:, 0])
        top_point_y = numpy.min(box[:, 1])
        bottom_point_y = numpy.max(box[:, 1])
        left_point_y = box[:, 1][numpy.where(box[:, 0] == left_point_x)][0]
        right_point_y = box[:, 1][numpy.where(box[:, 0] == right_point_x)][0]
        top_point_x = box[:, 0][numpy.where(box[:, 1] == top_point_y)][0]
        bottom_point_x = box[:, 0][numpy.where(box[:, 1] == bottom_point_y)][0]
        height = bottom_point_x - top_point_x
        width = right_point_x - left_point_x
        return height, width

        
def get_corners(img):
    colored = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    dst = cv2.cornerHarris(img,2,3,0.04)
    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)
    # Threshold for an optimal value, it may vary depending on the image.

    colored[dst>0.1*dst.max()]=[0,0,255]
    return colored


def test_video(video = "data/videos/placa_3.mp4"):
    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        exit()

    fge = StaticForegroundExtractor("models/bg_model/bg.png")
    result = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc('M','P','G','4'), 25, (1280,720*2) )

    ret, frame = cap.read()
    k = 0
    while frame is not None and k != 27:
        
        foreground = fge.extract_foreground(frame)
        with_corners = get_corners(foreground)
        
        concated = cv2.vconcat([frame, with_corners])
        cv2.imshow("fg", concated)
        result.write(concated)
        k = cv2.waitKey(1)
        
        ret, frame = cap.read()
    
    result.release()
    cap.release()

def test_image(imagePath = "data/images/fge_test.png", roiList = [[400, 294, 388, 112]]):
    fge = StaticForegroundExtractor("models/bg_model/bg.png")
    img = cv2.imread(imagePath)
    fg = fge.extract_foreground(image)
    measurements = fge.get_measurements_from_roi(fg, roiList)
    print(measurements)
    

if __name__=="__main__":
    test_image()