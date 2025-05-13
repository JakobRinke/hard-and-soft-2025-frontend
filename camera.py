import cv2

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)


    def __del__(self):
        self.video.release()

    def get_frame(self):
        # Ensure the video capture is opened
        if not self.video.isOpened():
            self.video.open(0)
        # ignore errors and logs of opencsv
        cv2.setLogLevel(0)

        success, image = self.video.read()
        if not success:
            return b''  # Return empty bytes instead of None
        else:
            # Resize the image to make it smaller
            resized_image = cv2.resize(image, (160, 120))  # Resize to 160x120
            ret, jpeg = cv2.imencode('.jpg', resized_image)
            return jpeg.tobytes()