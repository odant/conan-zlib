from conans import ConanFile, CMake, tools
import os, glob


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.11"
    license = "http://www.zlib.net/zlib_license.html"
    description = "A Massively Spiffy Yet Delicately Unobtrusive Compression Library " \
                  "(Also Free, Not to Mention Unencumbered by Patents)"
    url = "https://github.com/odant/conan-zlib"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [False, True], "minizip": [False, True], "dll_sign": [False, True], "fPIC": [False, True]}
    default_options = "shared=False", "minizip=True", "dll_sign=True", "fPIC=True"
    generators = "cmake"
    exports_sources = "src/*", "CMakeLists.txt", "FindZLIB.cmake", "minizip.patch"
    no_copy_source = True
    build_policy = "missing"
    
    def configure(self):
        # DLL sign
        if self.settings.os != "Windows" or not self.options.shared:
            self.options.dll_sign = False
        # Position indepent
        if self.settings.os == "Windows":
            self.options.fPIC = False
        elif self.options.shared:
            self.options.fPIC = True
        # Pure C library
        del self.settings.compiler.libcxx
    
    def build_requirements(self):
        if self.options.dll_sign:
            self.build_requires("find_windows_signtool/[~=1.0]@%s/stable" % self.user)
    
    def source(self):
        tools.patch(patch_file="minizip.patch")

    def build(self):
        # Build and install to package folder
        cmake = CMake(self, parallel=True)
        cmake.definitions["ENABLE_MINIZIP:BOOL"] = self.options.minizip
        cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE:BOOL"] = self.options.fPIC
        cmake.configure()
        cmake.build()

        # Remove unused files
        removable = []
        if self.options.shared:
            pattern = os.path.join(self.package_folder, "lib", "*static*")
            removable += glob.glob(pattern)
            pattern = os.path.join(self.package_folder, "lib", "*.a")
            removable += glob.glob(pattern)
        else:
            pattern = os.path.join(self.package_folder, "lib", "zlib.lib")
            removable += glob.glob(pattern)
            pattern = os.path.join(self.package_folder, "lib", "zlibd.lib")
            removable += glob.glob(pattern)
            pattern = os.path.join(self.package_folder, "lib", "minizip.lib")
            removable += glob.glob(pattern)
            pattern = os.path.join(self.package_folder, "lib", "minizipd.lib")
            removable += glob.glob(pattern)
            pattern = os.path.join(self.package_folder, "lib", "*.so*")
            removable += glob.glob(pattern)
            pattern = os.path.join(self.package_folder, "bin", "*.dll")
            removable += glob.glob(pattern)
        for fpath in removable:
            self.output.info("Remove %s" % fpath)
            os.remove(fpath)
        # Sign DLL
        if self.options.dll_sign:
            with tools.pythonpath(self):
                from find_windows_signtool import find_signtool
                signtool = '"' + find_signtool(str(self.settings.arch)) + '"'
                params =  "sign /a /t http://timestamp.verisign.com/scripts/timestamp.dll"
                pattern = os.path.join(self.package_folder, "bin", "*.dll")
                for fpath in glob.glob(pattern):
                    self.output.info("Sign %s" % fpath)
                    self.run("%s %s %s" %(signtool, params, fpath))
        
    def package(self):
        self.copy("FindZLIB.cmake", dst=".", src=".")
        # Headers
        self.copy("*zlib.h", dst="include", keep_path=False)
        self.copy("*zconf.h", dst="include", keep_path=False)
        self.copy("*zip.h", dst="include/minizip", keep_path=False)
        self.copy("*unzip.h", dst="include/minizip", keep_path=False)
        self.copy("*minizip_extern.h", dst="include/minizip", keep_path=False)
        self.copy("*crypt.h", dst="include/minizip", keep_path=False)
        self.copy("*mztools.h", dst="include/minizip", keep_path=False)
        self.copy("*ioapi.h", dst="include/minizip", keep_path=False)
        if self.settings.os == "Windows":
            self.copy("*iowin32.h", dst="include/minizip", keep_path=False)
        # Libraries
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False, symlinks=True)
        self.copy("*.a", dst="lib", keep_path=False)
        # PDB
        self.copy("*zlib.pdb", dst="bin", keep_path=False)
        self.copy("*zlibd.pdb", dst="bin", keep_path=False)
        self.copy("*minizip.pdb", dst="bin", keep_path=False)
        self.copy("*minizipd.pdb", dst="bin", keep_path=False)
        self.copy("*zlibstatic.pdb", dst="bin", keep_path=False)
        self.copy("*zlibstaticd.pdb", dst="bin", keep_path=False)
        self.copy("*minizipstatic.pdb", dst="bin", keep_path=False)
        self.copy("*minizipstaticd.pdb", dst="bin", keep_path=False)

    def package_info(self):
        libs = None
        if self.settings.os == "Windows":
            libs = ["zlib", "minizip"] if self.options.minizip else ["zlib"]
            if self.options.shared:
                self.cpp_info.defines = ["ZLIB_DLL", "MINIZIP_DLL"] if self.options.minizip else ["ZLIB_DLL"]
            else:
                libs = [i + "static" for i in libs]
            if self.settings.build_type == "Debug":
                libs = [i + "d" for i in libs]
        else:
            libs = ["z", "minizip"] if self.options.minizip else ["z"]
        self.cpp_info.libs = libs

