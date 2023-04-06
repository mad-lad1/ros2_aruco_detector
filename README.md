# ros2_aruco_detector
ros2 library for detecting AruCo tags without a camera matrix from a ZED camera.

To run the node, you must first launch the zed_wrapper using

```
ros2 launch zed_wrapper zed.launch.py
```

and then to run the detector, please run

```
ros2 run tag_detector aruco_detector
