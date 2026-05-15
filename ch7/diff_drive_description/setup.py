from setuptools import find_packages, setup

package_name = 'diff_drive_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['urdf/diff_drive_macro.xacro']),
        ('share/' + package_name, ['urdf/diff_drive.xacro']),
        #### Dùng 2 dòng lệnh sau ở ví dụ tiếp theo
        # ('share/' + package_name, ['urdf/diff_drive_with_lidar.xacro']),
        # ('share/' + package_name, ['urdf/diff_drive_with_lidar_control.xacro']),
        ('share/' + package_name, ['launch/display.launch.py']),
        #('share/' + package_name, ['launch/diff_drive_gazebo.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
