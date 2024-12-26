from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.scm import Git
from conan.tools.files import copy
import os

class ImguiDockingRecipe(ConanFile):
    name = "imguidocking"
    version = "2.0"
    package_type = "library"
    license = "Apache-2.0"
    homepage = "https://github.com/engine3d-dev/imgui"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [False, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = ["CMakeLists.txt", "imconfig.h", "imgui_internal.h", "imgui.h", "imstb_rectpack.h", "imstb_textedit.h", "imstb_truetype.h", "backend/imgui_impl_opengl3.h", "backends/imgui_impl_glfw.h", "backends/imgui_impl_glut.h", "backends/imgui_impl_vulkan.h", "backends/imgui_impl_win32.h"]
    # exports_sources = "*.h", "*.cpp", "backend/*.h"

    def requirements(self):
        self.requires("make/4.4.1")
        self.tool_requires("cmake/3.27.1")
        self.requires("glfw/3.4", transitive_headers=True)
        self.requires("opengl/system", transitive_headers=True)
        self.requires("vulkan-loader/1.3.290.0")

    def export_sources(self):
        copy(self, "CMakeLists.txt", self.recipe_folder, self.export_sources_folder)
        copy(self, "*.h", self.recipe_folder, self.export_sources_folder)
        copy(self, "*.cpp", self.recipe_folder, self.export_sources_folder)
        copy(self, "backend/*.h", self.recipe_folder, self.export_sources_folder)
        copy(self, "backends/*.cpp", self.recipe_folder, self.export_sources_folder)

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        # If you use "MinGW Makefiles" on windows, by default looks for mingw32-make.exe instead.
        # Needed to find make.exe installed by choco
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        # Copying *.h and *.cpp to a conan/imgui<hash>/p/imgui -> *.h
        print(f"[IMGUI] Package Folder = {self.package_folder}\n\n")
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, pattern="*.h", src=os.path.join(self.source_folder, "."), dst=os.path.join(self.package_folder, "."))
        copy(self, pattern="backends/*.h", src=os.path.join(self.source_folder, "."), dst=os.path.join(self.package_folder, "imgui"))
        # copy(self, pattern="*.cpp", src=os.path.join(self.source_folder, "."), dst=os.path.join(self.package_folder, "imgui"))
        copy(self, pattern="backends/*.h", src=os.path.join(self.source_folder, "backends"), dst=os.path.join(self.package_folder, "backends"))
        copy(self, pattern="imgui_impl_glfw.h", src=os.path.join(self.source_folder, "backends"), dst=os.path.join(self.package_folder, "backends"))
        copy(self, pattern="imgui_impl_vulkan.h", src=os.path.join(self.source_folder, "backends"), dst=os.path.join(self.package_folder, "backends"))
        # copy(self, pattern="*.cpp", src=os.path.join(self.source_folder, "backends"), dst=os.path.join(self.package_folder, "imgui/backends"))
        # copy(self, pattern="backends/imgui_impl_glfw.h", src=os.path.join(self.source_folder, "./backends/"), dst=os.path.join(self.package_folder, "imgui/backends"))
        # copy(self, pattern="backends/imgui_impl_vulkan.h", src=os.path.join(self.source_folder, "./backends/"), dst=os.path.join(self.package_folder, "imgui/backends"))
        # copy(self, pattern="backends/imgui_impl_glfw.cpp", src=os.path.join(self.source_folder, "./backends/"), dst=os.path.join(self.package_folder, "imgui/backends"))
        # copy(self, pattern="backends/imgui_impl_vulkan.cpp", src=os.path.join(self.source_folder, "./backends/"), dst=os.path.join(self.package_folder, "imgui/backends"))
        copy(self, pattern="*.a", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.so", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.lib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.dll", src=self.build_folder, dst=os.path.join(self.package_folder, "bin"), keep_path=False)
        copy(self, pattern="*.dylib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_target_name", "imguidocking::imguidocking")
        self.cpp_info.libs = ["imgui"]
        self.cpp_info.includedirs = ['./', './backends']  # Ordered list of include paths