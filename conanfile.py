from conans import ConanFile, CMake, tools


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.11"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "Description of Zlib"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "toolset": ["v140", "v141"]}
    default_options = "shared=False"
    generators = "cmake"
    exports_sources = "src/*"
	
    def source(self):
        tools.replace_in_file("src/CMakeLists.txt", "project(zlib C)", '''project(zlib C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            self.run('cmake %s/src -T %s %s' % (self.source_folder, self.options.toolset, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("zlib.h", dst="include", src="src")
        self.copy("zutil.h", dst="include", src="src")
        self.copy("zconf.h", dst="include", src=".")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ['zlib']
            if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
                self.cpp_info.libs[0] += "d"
        else:
            self.cpp_info.libs = ['z']
