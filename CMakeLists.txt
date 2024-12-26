cmake_minimum_required(VERSION 3.27)

project(imgui LANGUAGES CXX)

set(
    ALL_SRC
    imconfig.h
    imgui_internal.h
    imgui.h
    imstb_rectpack.h
    imstb_textedit.h
    imstb_truetype.h
    backends/imgui_impl_opengl3.h
    backends/imgui_impl_glfw.h
    # backends/imgui_impl_glut.h
    backends/imgui_impl_vulkan.h


    imgui.cpp
    imgui_demo.cpp
    imgui_draw.cpp
    imgui_tables.cpp
    imgui_widgets.cpp

    backends/imgui_impl_opengl3.cpp
    backends/imgui_impl_glfw.cpp
    # backends/imgui_impl_glut.cpp
    backends/imgui_impl_vulkan.cpp
#     backends/imgui_impl_metal.h
#     backends/imgui_impl_metal.mm
# endif()
    # backends/imgui_impl_opengl2.h
    # backends/imgui_impl_opengl3_loader.h

    # backends/imgui_impl_allegro5.h
    # backends/imgui_impl_android.h
    # backends/imgui_impl_dx9.h
    # backends/imgui_impl_dx10.h
    # backends/imgui_impl_dx11.h
    # backends/imgui_impl_dx12.h

    # backends/imgui_impl_osx.h
    # backends/imgui_impl_sdl2.h
    # backends/imgui_impl_sdl3.h
    # backends/imgui_impl_sdlrenderer2.h
    # backends/imgui_impl_sdlrenderer3.h
    # backends/imgui_impl_wgpu.h

    # backends/imgui_impl_allegro5.cpp
    # backends/imgui_impl_android.cpp
    # backends/imgui_impl_dx9.cpp
    # backends/imgui_impl_dx10.cpp
    # backends/imgui_impl_dx11.cpp
    # backends/imgui_impl_dx12.cpp

    # backends/imgui_impl_osx.mm
    # backends/imgui_impl_sdl2.cpp
    # backends/imgui_impl_sdl3.cpp
    # backends/imgui_impl_sdlrenderer2.cpp
    # backends/imgui_impl_sdlrenderer3.cpp
    # backends/imgui_impl_wgpu.cpp
)

# Adding sources that are dependent on OS.
if(WIN32)
    list(APPEND ALL_SRC backends/imgui_impl_win32.h backends/imgui_impl_win32.cpp)
elseif(APPLE)
    list(APPEND ALL_SRC backends/imgui_impl_metal.h backends/imgui_impl_metal.mm)
elseif(UNIX AND NOT APPLE)
    # Linux Support for ImGui
endif()

if(UNIX AND NOT APPLE)
    find_package(VulkanLoader REQUIRED CONFIG)
else()
    find_package(glfw3 REQUIRED)
    find_package(Vulkan REQUIRED)
endif()

add_library(${PROJECT_NAME} ${ALL_SRC})

target_include_directories(${PROJECT_NAME} PUBLIC ./)

# target_link_libraries(${PROJECT_NAME} glfw Vulkan::Vulkan)

if(WIN32)
target_link_libraries(${PROJECT_NAME} glfw Vulkan::Vulkan vulkan-headers::vulkan-headers)
elseif(UNIX AND NOT APPLE)
target_link_libraries(${PROJECT_NAME} glfw Vulkan::Loader vulkan-headers::vulkan-headers)
elseif(APPLE)
target_link_libraries(${PROJECT_NAME} glfw Vulkan::Vulkan vulkan-headers::vulkan-headers)
endif()

install(TARGETS ${PROJECT_NAME})
