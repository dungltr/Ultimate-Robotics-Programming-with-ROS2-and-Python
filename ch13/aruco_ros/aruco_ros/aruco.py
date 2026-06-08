import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import cv2
import numpy as np
from scipy.spatial.transform import Rotation as R
class ArucoMarkerNode(Node):
    def __init__(self):
        super().__init__('aruco_marker_node')
        self.image_subscriber = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)
        self.camera_info_subscriber = self.create_subscription(
            CameraInfo, '/camera_info', self.camera_info_callback, 10)
        # Publisher này sẽ gửi ảnh đã xử lý tới rqt_image_view
        self.image_pub = self.create_publisher(Image, '/aruco_markers_output', 10)
        self.bridge = CvBridge()
        self.camera_matrix = None
        self.dist_coeffs = None
        self.got_camera_info = False
        #self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
        # Thay dòng cũ bằng:
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
        self.aruco_params = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)
        self.get_logger().info("Aruco Marker Node đã khởi động!")
    def camera_info_callback(self, msg: CameraInfo):
        self.camera_matrix = np.array(msg.k).reshape((3, 3))
        self.dist_coeffs = np.array(msg.d)
        self.got_camera_info = True
    def image_callback(self, msg: Image):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        if not self.got_camera_info:
            h, w = cv_image.shape[:2]
            self.camera_matrix = np.array([[800, 0, w/2], [0, 800, h/2], [0, 0, 1]], dtype=np.float32)
            self.dist_coeffs = np.zeros((5, 1))
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = self.detector.detectMarkers(gray_image)
        # Làm mờ ảnh để loại bỏ nhiễu hạt trước khi nhận diện
        #gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0) 
        #corners, ids, rejected = self.detector.detectMarkers(gray_image)
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(cv_image, corners, ids)
            # Định nghĩa kích thước marker (ví dụ 0.1m)
            marker_size = 0.1
            obj_points = np.array([[-marker_size/2, marker_size/2, 0],
                                  [marker_size/2, marker_size/2, 0],
                                  [marker_size/2, -marker_size/2, 0],
                                  [-marker_size/2, -marker_size/2, 0]], dtype=np.float32)
            for i, corner in zip(ids, corners):
                # Sử dụng solvePnP để thay thế cho estimatePoseSingleMarkers đã bị xóa
                _, rvec, tvec = cv2.solvePnP(obj_points, corner, self.camera_matrix, self.dist_coeffs, False, cv2.SOLVEPNP_IPPE_SQUARE)
                # Vẽ trục tọa độ
                cv2.drawFrameAxes(cv_image, self.camera_matrix, self.dist_coeffs, rvec, tvec, 0.1)
                # In thông tin
                self.get_logger().info(f"ID: {i[0]} | Pos: {tvec.flatten()}")
        # Gửi ảnh đã xử lý lên topic
        msg_out = self.bridge.cv2_to_imgmsg(cv_image, encoding="bgr8")
        self.image_pub.publish(msg_out)
def main(args=None):
    rclpy.init(args=args)
    node = ArucoMarkerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()
