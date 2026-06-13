## Useful commands
```
ros2 launch tomauto1_description display.launch.xml

ros2 launch base_4wd_bringup base_4wd.launch.xml
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_drive_controller/cmd_vel -p stamped:=true
```
## Run terminator layout
```
terminator -l launch_ros
```

## ~/.config/terminator/config

```
[global_config]
  suppress_multiple_term_dialog = True
[keybindings]
[profiles]
  [[default]]
[layouts]
  [[default]]
    [[[window0]]]
      type = Window
      parent = ""
    [[[child1]]]
      type = Terminal
      parent = window0
  [[launch_4wd]]
    [[[window0]]]
      type = Window
      parent = ""
    [[[child1]]]
      type = VPaned
      parent = window0
    [[[terminal1]]]
      type = Terminal
      parent = child1
      profile = default
      command = bash -c "cd /home/daniel/projects/foodlikeair/baseline_4wd; ros2 launch base_4wd_bringup base_4wd.gazebo.launch.xml; exec bash"
    [[[terminal2]]]
      type = Terminal
      parent = child1
      profile = default
      command = basimageviewh -c "cd /home/daniel/projects/foodlikeair/baseline_4wd; ros2 run teleop_twist_keyboard teleop_twist_keyboard; exec bash"
[plugins]
``` 

## System dependencies
- ROS2
- opencv-python


## Commands
`ros2 launch base_4wd_bringup base_4wd.gazebo.launch.xml`
`ros2 run teleop_twist_keyboard teleop_twist_keyboard`
`ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True`
`ros2 launch nav2_bringup bringup_launch.py map:=/home/daniel/projects/foodlikeair/baseline_4wd/src/base_4wd_bringup/maps/dpt3/dpt3.yaml use_sim_time:=True`

## To start with nav2 manually for navigation run simply
1. `ros2 launch base_4wd_bringup base_4wd.gazebo.launch.xml`
2. `ros2 launch nav2_bringup bringup_launch.py map:=/home/daniel/projects/foodlikeair/baseline_4wd/src/base_4wd_bringup/maps/dpt3/dpt3.yaml use_sim_time:=True`
3. The set 2d pose estimate

## To start mapping
1. `ros2 launch base_4wd_bringup base_4wd_cartophgrapher.launch.xml`
2. Drive around create the map
3. `ros2 run nav2_map_server map_saver_cli -f /path/to/my_map`

## Useful resources
1. Lidar code: https://github.com/ldrobotSensorTeam/ldlidar_stl_ros2/tree/master/ldlidar_driver