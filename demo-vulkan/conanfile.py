from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.scm import Git
from conan.tools.files import copy
import os

class Demo(ConanFile):
    name = "demovulkan"
    version = "1.0"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "CMakeLists.txt", "main.cpp"

    def requirements(self):
        # self.requires("engine3d-cmake-utils/2.0")
        self.tool_requires("engine3d-cmake-utils/2.0")
        self.requires("glfw/3.4", transitive_headers=True)
        self.requires("opengl/system", transitive_headers=True)

        # These end in 1.0 because they are engine3d-customized conan packages
        # Slighly modified of the conan packages and it's CMake generators to using "Unix Makefiles" 
        self.requires("fmt/10.2.1", transitive_headers=True)
        self.requires("spdlog/1.14.1", transitive_headers=True)
        self.requires("glm/1.0.1", transitive_headers=True)
        self.requires("yaml-cpp/0.8.0", transitive_headers=True)
        self.requires("entt/3.13.2")
        self.requires("box2d/2.4.2")
        self.requires("joltphysics/1.0")
        self.requires("vulkan-headers/1.3.290.0")

        if self.settings.os == "Linux":
            self.requires("vulkan-loader/1.3.290.0")
        
        self.requires("imguidocking/2.0")
        print(f"OS = {self.settings.os}")      

    def generate(self):
        cmake = CMakeDeps(self)
        cmake.generate()
        tc = CMakeToolchain(self, generator="Unix Makefiles")
        tc.generate()
    
    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
    
    def layout(self):
        cmake_layout(self)
    
    # def package(self):
    #     copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
    #     copy(self, pattern="*.h", src=os.path.join(self.source_folder, "./"), dst=os.path.join(self.package_folder, "Testbed"))
    #     copy(self, pattern="*.a", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
    #     copy(self, pattern="*.so", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
    #     copy(self, pattern="*.lib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
    #     copy(self, pattern="*.dll", src=self.build_folder, dst=os.path.join(self.package_folder, "bin"), keep_path=False)
    #     copy(self, pattern="*.dylib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
    #     cmake = CMake(self)
    #     cmake.install()