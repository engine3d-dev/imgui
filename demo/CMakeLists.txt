cmake_minimum_required(VERSION 3.15)
project(Testbed CXX)

find_package(imguidocking REQUIRED)

add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(
    ${PROJECT_NAME}
    imguidocking::imguidocking
)