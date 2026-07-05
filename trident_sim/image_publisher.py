#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np


class ImagePublisher(Node):
    def __init__(self):
        super().__init__('trident_image_publisher')

        self.rgb_pub = self.create_publisher(
            Image, '/trident/rgb/image_raw', 10)
        self.thermal_pub = self.create_publisher(
            Image, '/trident/thermal/image_raw', 10)

        self.bridge = CvBridge()
        self.frame_count = 0

        self.create_timer(1.0/30.0, self.publish_rgb)
        self.create_timer(1.0/15.0, self.publish_thermal)

        self.get_logger().info('TRIDENT image publisher started')

    def publish_rgb(self):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[:] = (80, 80, 80)

        offset = (self.frame_count * 2) % 640
        human_x = (200 + offset) % 580
        human_y = 180

        cv2.rectangle(frame,
                      (human_x, human_y),
                      (human_x + 40, human_y + 80),
                      (180, 120, 80), -1)

        cv2.circle(frame,
                   (human_x + 20, human_y - 15),
                   15, (180, 120, 80), -1)

        cv2.putText(frame, f'TRIDENT RGB | Frame {self.frame_count}',
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (255, 255, 255), 1)

        if self.frame_count % 30 == 0:
            cv2.imwrite(f'/tmp/trident_rgb_{self.frame_count}.png', frame)

        self.frame_count += 1

        msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'rgb_camera_link'
        self.rgb_pub.publish(msg)

    def publish_thermal(self):
        frame = np.zeros((240, 320), dtype=np.uint8)
        frame[:] = 40

        noise = np.random.randint(0, 15, (240, 320), dtype=np.uint8)
        frame = cv2.add(frame, noise)

        offset = (self.frame_count * 1) % 280
        human_x = (100 + offset) % 260
        human_y = 90

        cv2.rectangle(frame,
                      (human_x, human_y),
                      (human_x + 20, human_y + 40),
                      220, -1)

        cv2.circle(frame,
                   (human_x + 10, human_y - 8),
                   8, 240, -1)

        frame = cv2.GaussianBlur(frame, (5, 5), 0)

        cv2.putText(frame, f'TRIDENT THERMAL',
                    (5, 15), cv2.FONT_HERSHEY_SIMPLEX,
                    0.4, (255), 1)

        if self.frame_count % 30 == 0:
            cv2.imwrite(f'/tmp/trident_thermal_{self.frame_count}.png', frame)

        msg = self.bridge.cv2_to_imgmsg(frame, encoding='mono8')
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'thermal_camera_link'
        self.thermal_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ImagePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()