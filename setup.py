from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'slinam_node'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py')),
        (os.path.join('config', package_name), glob('config/*.yaml'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='SpaceSoarer90',
    maintainer_email='josequintusxavier@gmail.com',
    description='Slinam Robot DSTF Robotics Group Team',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'slinam_serial = slinam_node.slinam_serial:main',
        ],
    },
)
