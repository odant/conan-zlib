from conans import ConanFile, CMake
import os

class PackageTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def isClangClToolset(self):
        return True if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio" and str(self.settings.compiler.toolset).lower() == "clangcl" else False

    def build_requirements(self):
        if not self.isClangClToolset():
            self.build_requires("ninja/[>=1.10.2]")

    def build(self):
        cmakeGenerator = "Ninja" if not self.isClangClToolset() else None
        cmake = CMake(self, generator=cmakeGenerator)
        cmake.definitions["ENABLE_MINIZIP:BOOL"] = self.options["zlib"].minizip
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.pdb", dst="bin", src="bin")
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.so.*", dst="bin", src="lib")

    def test(self):
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            self.run("ctest --output-on-failure --build-config %s" % self.settings.build_type)
        else:
            self.run("ctest --output-on-failure")
