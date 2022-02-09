import cv2
import time


class StopLineDetector:

    def __init__(self):
        self.first_frame = True
        self.previous_frame = None
        self.stop_time = 0
        self.production_time = 0
        self.fps = 30

    def set_video_fps(self, video_fps):
        self.fps = video_fps

    def execute(self, frame):

        line_status = 'Stop'
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.first_frame:
            self.first_frame = False

        else:
            frame_delta = cv2.absdiff(self.previous_frame, gray)
            threshold = cv2.threshold(frame_delta, 50, 255, cv2.THRESH_BINARY)[1]
            threshold = cv2.dilate(threshold, None, iterations=2)
            contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)[0]

            for contour in contours:

                if cv2.contourArea(contour) > 150:
                    line_status = 'Production'

            if line_status == 'Production':
                self.production_time += 1 / self.fps
            else:
                self.stop_time += 1 / self.fps

        self.previous_frame = gray

        cv2.putText(frame, "Line Status: {}".format(line_status), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, "Productive Time: {:.2f}".format(self.production_time), (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, "Stopped Time: {:.2f}".format(self.stop_time), (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        if line_status == 'Stop':
            line_stopped = True
        else:
            line_stopped = False

        return frame, line_stopped
