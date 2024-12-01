import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/mint/Documents/ros/workspaces/slinam_ws/src/slinam_nodes/install/slinam_node'
