cmake_minimum_required(VERSION 3.20)
project(VulkanDemo CXX)

find_package(Vulkan REQUIRED)
find_package(imguidocking REQUIRED)

add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(
    ${PROJECT_NAME}
    Vulkan::Vulkan
    imguidocking::imguidocking
)