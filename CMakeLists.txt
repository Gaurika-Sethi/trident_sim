cmake_minimum_required(VERSION 3.8)
project(trident_sim)

find_package(ament_cmake REQUIRED)

# Install directories
install(DIRECTORY
  worlds
  models
  launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()