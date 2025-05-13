import cv2
try:
    import rospy
    from sensor_msgs.msg import Image
    from cv_bridge import CvBridge
except:
    pass

class VideoCamera(object):
    def __init__(self):
        # Initialisiere ROS Node
        rospy.init_node('ros_camera_listener', anonymous=True)
        
        # Erstelle einen CvBridge-Objekt zum Konvertieren von ROS-Nachrichten in OpenCV-Bilder
        self.bridge = CvBridge()

        # Initialisiere VideoCapture mit 0 für /dev/video0 (Falle zurück, falls ROS nicht läuft)
        self.video = None
        self.image_sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.image_callback)
        self.current_frame = None

    def image_callback(self, msg):
        """Callback-Funktion zum Empfangen von Bildern von ROS"""
        try:
            # Konvertiere das ROS Bild in ein OpenCV Bild
            self.current_frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            print(f"Fehler bei der Bildkonvertierung: {e}")

    def __del__(self):
        if self.video is not None:
            self.video.release()

    def get_frame(self):
        # Falls der ROS Stream verfügbar ist, verwende ihn
        if self.current_frame is not None:
            # Resize das Bild, wenn du möchtest
            resized_image = cv2.resize(self.current_frame, (160, 120))
            ret, jpeg = cv2.imencode('.jpg', resized_image)
            return jpeg.tobytes()

        # Wenn ROS nicht verfügbar ist oder kein Bild empfangen wurde, greife auf /dev/video0 zurück
        if self.video is None:
            self.video = cv2.VideoCapture(0)  # Öffne /dev/video0 als Fallback

        if self.video.isOpened():
            success, image = self.video.read()
            if not success:
                return b''  # Return empty bytes instead of None
            else:
                resized_image = cv2.resize(image, (160, 120))  # Resize to 160x120
                ret, jpeg = cv2.imencode('.jpg', resized_image)
                return jpeg.tobytes()

        return b''  # Falls keine Kamera verfügbar ist, gib leere Bytes zurück
