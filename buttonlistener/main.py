import rclpy
from rclpy.node import Node
from pynput import keyboard
from std_msgs.msg import Bool

class KeyPressNode(Node):

    def __init__(self):
        super().__init__('keyboard_listener_node')
        self.publisher_ = self.create_publisher(Bool, '/keypress_status', 10)
        
        # Start the keyboard listener
        self.listener = keyboard.Listener(on_press=self.monitor_keypress)
        self.listener.start()

    def monitor_keypress(self, key):
        try:
            if key.char == 'b':
                self.publish_keypress(True)
            elif key.char == 'c':
                self.publish_keypress(False)
        except AttributeError:
            pass
    
    def publish_keypress(self, value):
        msg = Bool()
        msg.data = value
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = KeyPressNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.listener.stop()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
