import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    urdf_path = os.path.join(get_package_share_directory('tomauto1_description'), 'urdf', 'tomauto1.urdf.xacro')
    gazebo_config_path = os.path.join(get_package_share_directory('tomauto1_bringup'), 'config', 'gazebo_bridge.yaml')
    rviz_config_path = os.path.join(get_package_share_directory('tomauto1_description'), 'rviz', 'nav2_lidar.rviz')
    nav2_params_path = os.path.join(get_package_share_directory('tomauto1_bringup'), 'config', 'nav2_params.yaml')
    map_path = '/home/daniel/projects/foodlikeair/tomauto1/src/tomauto1_bringup/maps/dpt3/dpt3.yaml'
    world_path = os.path.join(get_package_share_directory('tomauto1_bringup'), 'worlds', 'dpt3.sdf')

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', urdf_path]),
            'use_sim_time': True
        }]
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('ros_gz_sim'), '/launch/gz_sim.launch.py'
        ]),
        launch_arguments={'gz_args': world_path + ' -r'}.items()
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description']
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': gazebo_config_path}]
    )

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager']
    )

    diff_drive_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['diff_drive_controller', '--controller-manager', '/controller_manager'],
        remappings=[
            ('/diff_drive_controller/odom', '/odom'),
            ('/diff_drive_controller/cmd_vel', '/cmd_vel'),
        ]
    )

    twist_stamper = Node(
        package='twist_stamper',
        executable='twist_stamper',
        name='twist_stamper',
        parameters=[{'frame_id': 'base_link'}],
        remappings=[
            ('cmd_vel_in', '/cmd_vel'),
            ('cmd_vel_out', '/diff_drive_controller/cmd_vel')
        ]
    )

    # fox_glove = Node(
    #     package='foxglove_bridge',
    #     executable='foxglove_bridge',
    #     parameters=[{
    #         'use_sim_time': True,
    #         'port': 8765,
    #     }]
    # )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_path]
    )

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('nav2_bringup'), '/launch/bringup_launch.py'
        ]),
        launch_arguments={
            'map': map_path,
            'params_file': nav2_params_path,
            'use_sim_time': 'True'
        }.items()
    )

    odom_relay = Node(
        package='topic_tools',
        executable='relay',
        arguments=['/diff_drive_controller/odom', '/odom']
    )

    return LaunchDescription([
        robot_state_publisher,
        gazebo,
        spawn_robot,
        bridge,
        joint_state_broadcaster_spawner,
        diff_drive_spawner,
        twist_stamper,
        rviz,
        nav2,
        odom_relay
    ])