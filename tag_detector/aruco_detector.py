import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
import cv2.aruco as aruco
from cv_bridge import CvBridge

class TagDetectorSubcriber(Node):
    """
    A Node class that detects AruCo Markers 
    """
    def __init__(self, name, topic):
        super().__init__(name)
        self.subscription = self.create_subscription(
            Image,
            topic,
            self.image_callback, 10)
        
        self.bridge = CvBridge()
        self.detectorParams = aruco.DetectorParameters()
        self.aruco_dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
        self.aruco_detector = aruco.ArucoDetector(self.aruco_dictionary, self.detectorParams)

    def image_callback(self, msg):
        """
        Summary:
            Detects AruCo markers and shows them in a bounding box
            using OpenCV
        Args:
            msg: Image received from topic
        """
        self.get_logger().info("Receiving rectified images from ZED camera")
        image = self.bridge.imgmsg_to_cv2(msg, "bgr8")  # Add the encoding parameter
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        markerCorners, markerIds, rejectedCandidates = self.aruco_detector.detectMarkers(image_gray)
    

        # Start detecting tags
        if markerIds is not None:
            aruco.drawDetectedMarkers(image, markerCorners)  # Draw a square around the markers

        cv2.imshow('frame', image)
        key = cv2.waitKey(3) & 0xFF
        if key == ord('q'):  # Quit
            cv2.destroyAllWindows()

def main(args=None):
    print("Starting Node!")
    rclpy.init(args=args)
    topic_name = '/zed/zed_node/rgb/image_rect_color'
    tag_detector = TagDetectorSubcriber('aruco_detector', topic_name)
    rclpy.spin(tag_detector)
    tag_detector.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()
