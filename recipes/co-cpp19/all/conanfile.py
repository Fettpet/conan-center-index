from conans import ConanFile, CMake
from conan.tools.cmake import CMakeToolchain
from conans import tools
import os

class cocpp19Conan(ConanFile):
    name = "co-cpp19"
    version = "0.1.0"
    
    # Optional metadata
    license = "MIT License"
    author = "Hicknhack Software"
    url = "https://github.com/basicpp17/co-cpp19"
    description = "C++17/20 Library with the fastest runtime and compile times"
    topics = ("algorithm", "container", "common", "utility")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    @property
    def _source_subfolder(self):
        return "co-cpp19"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True, destination=self._source_subfolder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        cmake.build()

    def package(self):
        source_dir = os.path.join(self._source_subfolder, "src")
        include_dirs = [os.path.join(source_dir, name) for name in os.listdir(source_dir)]
        include_dirs = [name for name in include_dirs if os.path.isdir(name) ]
        for include_dir in include_dirs:
            self.copy("*.h", src=include_dir, dst="include")
        self.copy("*.lib", dst="lib", excludes="*gtest*", keep_path=False)
