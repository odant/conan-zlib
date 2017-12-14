from conans import ConanFile, CMake
import os


class ZlibTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        self.output.info("env: CONAN_PRINT_RUN_COMMANDS => %s" % os.getenv("CONAN_PRINT_RUN_COMMANDS", "Unset"))
        cmake = CMake(self, parallel=True)
        defs = {"ENABLE_MINIZIP:BOOL": self.options["zlib"].minizip}
        cmake.configure(defs=defs)
        cmake.build()

    def imports(self):
        self.copy("*.pdb", dst="bin", src="bin")
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def test(self):
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            self.run("ctest --output-on-failure --build-config %s" % self.settings.build_type)
        else:
            self.run("ctest --output-on-failure")
