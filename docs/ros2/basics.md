---
sidebar_position: 1
---

# ROS 2 Basics

The Robot Operating System 2 (ROS 2) is a flexible framework for writing robot software. It's not an operating system, but rather a collection of tools, libraries, and conventions to aid in creating robot applications. This section introduces the fundamental concepts of ROS 2.

## What is ROS 2?

ROS 2 is the evolution of the original ROS (Robot Operating System), designed to address limitations in the original system and enable deployment in production environments. It provides:

- A distributed computing framework for robot applications
- Standardized interfaces and tools for robot development
- Middleware for inter-process communication
- Package management and build systems
- Simulation capabilities

## Key Features of ROS 2

### Distributed Architecture
ROS 2 uses Data Distribution Service (DDS) as its middleware, enabling robust communication between processes and even across machines.

### Improved Real-Time Support
Enhanced capabilities for real-time systems compared to ROS 1.

### Security Features
Built-in security mechanisms for data encryption, authentication, and authorization.

### Professional Development
Better support for commercial robot development and deployment.

## Core Concepts

### Nodes
Nodes are individual processes that perform computation. In ROS 2:
- A single device may have multiple nodes
- Nodes communicate with each other
- Nodes are typically organized around computational tasks

Example of creating a minimal node in Python:
```python
import rclpy
from rclpy.node import Node

class MinimalNode(Node):
    def __init__(self):
        super().__init__('minimal_node')
        self.get_logger().info('Hello from minimal node!')

def main(args=None):
    rclpy.init(args=args)
    node = MinimalNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Topics and Messages
Topics are named buses over which nodes exchange messages:
- Publishers send messages to topics
- Subscribers receive messages from topics
- Multiple publishers and subscribers can use the same topic
- Communication is asynchronous

### Services
Services provide synchronous request/response communication:
- Services have types defining request and response structures
- One service server handles requests from multiple clients
- Useful for actions that return a result

### Actions
Actions are a more complex form of communication for long-running tasks:
- Goal/Result/Feedback pattern
- Cancel functionality
- Status reporting during execution

## Setting Up Your First Workspace

### Creating a Workspace

1. Create a workspace directory:
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

2. Build the workspace:
```bash
colcon build
```

3. Source the workspace:
```bash
source install/setup.bash
```

### Creating a Package

1. Navigate to your workspace:
```bash
cd ~/ros2_ws/src
```

2. Create a new package:
```bash
ros2 pkg create --build-type ament_python my_robot_package
```

3. Your package structure will look like:
```
my_robot_package/
├── my_robot_package/
├── setup.cfg
├── setup.py
├── package.xml
```

## Essential ROS 2 Commands

### Node Commands
- `ros2 run <package_name> <executable_name>` - Run a node
- `ros2 node list` - List active nodes
- `ros2 node info <node_name>` - Get information about a node

### Topic Commands
- `ros2 topic list` - List active topics
- `ros2 topic echo <topic_name>` - Print messages on a topic
- `ros2 topic pub <topic_name> <msg_type> <args>` - Publish messages to a topic
- `ros2 topic info <topic_name>` - Get information about a topic

### Service Commands
- `ros2 service list` - List active services
- `ros2 service call <service_name> <service_type> <arguments>` - Call a service

### Parameter Commands
- `ros2 param list` - List parameters of a node
- `ros2 param get <node_name> <param_name>` - Get a parameter value
- `ros2 param set <node_name> <param_name> <value>` - Set a parameter value

## ROS 2 Launch Files

Launch files allow you to start multiple nodes with a single command:

```xml
<launch>
  <node pkg="my_robot_package" exec="publisher_node" name="publisher"/>
  <node pkg="my_robot_package" exec="subscriber_node" name="subscriber"/>
</launch>
```

Or using Python launch files:
```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_robot_package',
            executable='publisher_node',
            name='publisher'
        ),
        Node(
            package='my_robot_package',
            executable='subscriber_node',
            name='subscriber'
        )
    ])
```

## Best Practices

### Package Organization
- Organize packages by functionality
- Follow naming conventions (lowercase, underscores)
- Use descriptive package names

### Node Design
- Design nodes to perform a single, well-defined task
- Make nodes reusable and configurable
- Handle errors gracefully

### Message Design
- Keep messages simple but informative
- Use meaningful field names
- Consider bandwidth and serialization overhead

### Testing
- Write unit tests for your nodes
- Use rostest for integration testing
- Test with realistic simulation scenarios

## Next Steps

With these basics covered, you're ready to dive deeper into specific ROS 2 concepts and start building your own robot applications. The next sections will explore advanced messaging patterns, parameter management, and integration with other tools in the robotics ecosystem.