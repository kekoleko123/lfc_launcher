# LFC Launcher

The goal of this small package is to launch properly the [linear_feedback_controller](https://github.com/loco-3d/linear-feedback-controller/tree/humble) on the Tiago Robot from PAL Robotics. It is working under ROS2 Humble. It can easily be used for other robot models by modifying the parameters files.

This package contains two configuration files (.yaml) and one launch file (.py).

## lfc_config.yaml

This configuraiton file contains the different arguments used by both the linear_feedback_control and the joint_state_estimator required for its functioning.

You can find more informations about the controllers parameters in the [joint_state_estimator.yaml file](https://github.com/loco-3d/linear-feedback-controller/blob/humble/src/joint_state_estimator.yaml) and in the [linear_feedback_controller.yaml file](https://github.com/loco-3d/linear-feedback-controller/blob/humble/src/linear_feedback_controller.yaml).

## lfc_launch.py

This launch file is used to start the controllers. It initially loads inactive the linear_feedback_controller, then the joint_state_estimator. Once they are loaded, the launch activate both controllers.

To run the launch file, source your workspace and use :

`ros2 launch lfc_launcher lfc_launch.py`

## pd_plus_controller_params.yaml

This configuration file contains the differents parameters for the pd_plus_controller node in the linear_feedback_controller package.

To run the test, you can then use the following command by replacing the `path/` by the path to lfc_launcher package:

`ros2 run linear_feedback_controller pd_plus_controller --ros-args --params-file path/config/pd_plus_controller_params.yaml`

If Tiago's arm is waving slighlty, then the linear feedback controller is operational.