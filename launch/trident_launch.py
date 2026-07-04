import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node


def generate_launch_description():

    pkg = get_package_share_directory('trident_sim')
    world_file = os.path.join(pkg, 'worlds', 'trident_world.sdf')
    urdf_file  = os.path.join(pkg, 'models',  'trident_drone.urdf')

    with open(urdf_file, 'r') as f:
        robot_desc = f.read()

    # 1. Launch Gazebo with the world
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', world_file],
        output='screen'
    )

    # 2. Robot state publisher — publishes /robot_description and TF
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # 3. Spawn drone into Gazebo (delayed 5s to let Gazebo fully load)
    spawn_drone = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='ros_gz_sim',
                executable='create',
                name='spawn_trident',
                output='screen',
                arguments=[
                    '-topic', '/robot_description',
                    '-name',  'trident_drone',
                    '-z',     '2.0'
                ]
            )
        ]
    )

    # 4. ROS-Gazebo bridge for camera topics
    bridge = TimerAction(
        period=7.0,
        actions=[
            Node(
                package='ros_gz_bridge',
                executable='parameter_bridge',
                name='gz_bridge',
                output='screen',
                arguments=[
                    '/trident/rgb/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
                    '/trident/thermal/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
                    '/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock',
                ]
            )
        ]
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_drone,
        bridge,
    ])