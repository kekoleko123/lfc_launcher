import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription, LaunchContext
from launch.launch_description_entity import LaunchDescriptionEntity
from launch.actions import GroupAction, ExecuteProcess, RegisterEventHandler, OpaqueFunction
from launch.event_handlers import OnProcessExit
from controller_manager.launch_utils import generate_load_controller_launch_description

def generate_launch_description():

    return LaunchDescription(
        [OpaqueFunction(function=launch_setup)]
    )

def launch_setup(
    context: LaunchContext, *args, **kwargs
) -> list[LaunchDescriptionEntity]:

    linear_feedback_controller_loader = generate_load_controller_launch_description(
        controller_name='linear_feedback_controller',
        controller_params_file=os.path.join(
            get_package_share_directory('lfc_launcher'), 'config', 'lfc_config.yaml'
        ),
        extra_spawner_args=["--inactive", "--controller-manager-timeout", "1000"],
    )

    joint_state_estimator_loader = generate_load_controller_launch_description(
        controller_name='joint_state_estimator',
        controller_params_file=os.path.join(
            get_package_share_directory('lfc_launcher'), 'config', 'lfc_config.yaml'
        ),
        extra_spawner_args=["--inactive", "--controller-manager-timeout", "1000"],
    )
    

    lfc_controllers_activator = ExecuteProcess(
        cmd=[
            "ros2",
            "service",
            "call",
            "/controller_manager/switch_controller",
            "controller_manager_msgs/srv/SwitchController",
            "{activate_controllers: ['joint_state_estimator', 'linear_feedback_controller'], stop_controllers: [], strictness: 2}",
        ],
        output="screen",
    )

    return [

        # Loading of the linear_feedback_controller
        linear_feedback_controller_loader,

        # Once it is done, loading of the joint_state_estimator controller
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=linear_feedback_controller_loader.entities[-1],
                on_exit=[joint_state_estimator_loader],
            )
        ),

        # Once it is done, activation of the two controllers
        # We do that to be sure that both controllers are loaded in the right order, and that they are activated AFTER their loading
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=joint_state_estimator_loader.entities[-1],
                on_exit=[lfc_controllers_activator],
            )
        )

    ]