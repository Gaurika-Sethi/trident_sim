cmake_minimum_required(VERSION 3.8)
project(trident_sim)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)

# Install Python package
ament_python_install_package(${PROJECT_NAME})

# Install Python scripts as executables
install(PROGRAMS
  trident_sim/image_publisher.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install directories
install(DIRECTORY
  worlds
  models
  launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()