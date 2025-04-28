from conan import ConanFile, tools
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.errors import ConanInvalidConfiguration, ConanException
from conan.tools import build, microsoft, scm, env, files  

import os, glob


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.3.1+0"
    license = "http://www.zlib.net/zlib_license.html"
    description = "A Massively Spiffy Yet Delicately Unobtrusive Compression Library " \
                  "(Also Free, Not to Mention Unencumbered by Patents)"
    url = "https://github.com/odant/conan-zlib"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared":   [False, True], 
        "minizip":  [False, True], 
        "dll_sign": [False, True],
        "fPIC":     [False, True]
    }
    default_options = {
        "shared":   False, 
        "minizip":  True, 
        "dll_sign": True, 
        "fPIC":     True
    }
    exports_sources = "src/*", "CMakeLists.txt"
    no_copy_source = True
    build_policy = "missing"
    package_type = "library"
    python_requires = "windows_signtool/[>=1.2]@odant/stable"
    
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            
    def layout(self):
        cmake_layout(self) 

    def configure(self):
        # DLL sign
        if self.settings.os != "Windows" or not self.options.shared:
            del self.options.dll_sign
        # Position independent code
        if self.options.shared:
            self.options.rm_safe("fPIC")
        # Pure C library
        self.settings.compiler.rm_safe("libcxx")
        self.settings.compiler.rm_safe("cppstd")
    
    def build_requirements(self):
        self.tool_requires("ninja/[>=1.12.1]")
    
    def generate(self):
        envir = env.VirtualBuildEnv(self);
        envir.generate();
        
        if microsoft.is_msvc(self):
            vcvars = microsoft.VCVars(self);
            vcvars.generate();
        
        tc = CMakeToolchain(self, generator="Ninja")
        tc.variables["ENABLE_MINIZIP"] = self.options.minizip
        tc.variables["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.get_safe("fPIC", True)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        
    def package(self):
        # Headers
        include = os.path.join(self.package_folder, "include")
        source = os.path.join(self.source_folder, "src")
        files.copy(self, "*zlib.h", dst=include, src=source, keep_path=False)
        files.copy(self, "*zconf.h", dst=include, src=os.path.join(self.build_folder, "src"), keep_path=False)
        if self.options.minizip:
            minizip_inc = os.path.join(include, "minizip")
            files.copy(self, "*zip.h", dst=minizip_inc, src=source, keep_path=False)
            files.copy(self, "*unzip.h", dst=minizip_inc, src=source, keep_path=False)
            files.copy(self, "*minizip_extern.h", dst=minizip_inc, src=source, keep_path=False)
            files.copy(self, "*crypt.h", dst=minizip_inc, src=source, keep_path=False)
            files.copy(self, "*mztools.h", dst=minizip_inc, src=source, keep_path=False)
            files.copy(self, "*ioapi.h", dst=minizip_inc, src=source, keep_path=False)
            if self.settings.os == "Windows":
                files.copy(self, "*iowin32.h", dst=minizip_inc, src=source, keep_path=False)
        # Libraries
        bin = os.path.join(self.package_folder, "bin")
        files.copy(self, "*.dll", dst=bin, src=self.build_folder, keep_path=False)
        lib = os.path.join(self.package_folder, "lib")
        files.copy(self, "*.lib", dst=lib, src=self.build_folder, keep_path=False)
        files.copy(self, "*.so*", dst=lib, src=self.build_folder, keep_path=False)
        files.copy(self, "*.a", dst=lib, src=self.build_folder, keep_path=False)
        
        if self.settings.os in ["Linux", "FreeBSD"] and self.options.shared:
            extension = "so"
            # Create libtbb.so.2 -> libtbb.so, etc symlinks
            with chdir(self, os.path.join(self.package_folder, "lib")):
                for fname in os.listdir("."):
                    fname_without_version = fname.split(f".{extension}", 1)[0] + f".{extension}"
                    self.run(f'ln -s "{fname}" "{fname_without_version}"')
                    
        # PDB
        files.copy(self, "*zlib.pdb", dst=bin, src=self.build_folder, keep_path=False)
        files.copy(self, "*zlibd.pdb", dst=bin, src=self.build_folder, keep_path=False)
        files.copy(self, "*minizip.pdb", dst=bin, src=self.build_folder, keep_path=False)
        files.copy(self, "*minizipd.pdb", dst=bin, src=self.build_folder, keep_path=False)
        files.copy(self, "*zlibstatic.pdb", dst=bin, src=self.build_folder, keep_path=False)
        files.copy(self, "*zlibstaticd.pdb", dst=bin, src=self.build_folder, keep_path=False)
        files.copy(self, "*minizipstatic.pdb", dst=bin, src=self.build_folder, keep_path=False)
        files.copy(self, "*minizipstaticd.pdb", dst=bin, src=self.build_folder, keep_path=False)
        # Sign DLL
        if self.options.get_safe("dll_sign"):
            self.python_requires["windows_signtool"].module.sign(self, [os.path.join(self.package_folder, "bin", "*.dll")])

    def package_info(self):
        self.cpp_info.set_property("cmake_target_name", "zlib::all")
        self.cpp_info.set_property("cmake_target_aliases", ["ZLIB::ALL"])
        self.cpp_info.set_property("cmake_find_mode", "both")
        
        zlib_libs = None
        if self.settings.os == "Windows":
            zlib_libs = ["zlib"]
            if not self.options.shared:
                zlib_libs = [i + "static" for i in zlib_libs]
            if self.settings.build_type == "Debug":
                zlib_libs = [i + "d" for i in zlib_libs]
        else:
            zlib_libs = ["z"]
        
        self.cpp_info.components["zlib"].set_property("cmake_target_name", "zlib::zlib")
        self.cpp_info.components["zlib"].set_property("cmake_target_aliases", ["ZLIB", "ZLIB::ZLIB"])
        self.cpp_info.components["zlib"].libs = zlib_libs
        if self.options.shared:
            self.cpp_info.components["zlib"].defines = ["ZLIB_DLL"]
        
        if self.options.minizip:
            minizip_libs = None
            if self.settings.os == "Windows":
                minizip_libs = ["minizip"]
                if not self.options.shared:
                    minizip_libs = [i + "static" for i in minizip_libs]
                if self.settings.build_type == "Debug":
                    minizip_libs = [i + "d" for i in minizip_libs]
            else:
                minizip_libs = ["minizip"]
            self.cpp_info.components["minizip"].set_property("cmake_target_name", "zlib::minizip")
            self.cpp_info.components["minizip"].set_property("cmake_target_aliases", ["ZLIB::MINIZIP"])
            self.cpp_info.components["minizip"].libs = minizip_libs
            if self.options.shared:
                self.cpp_info.components["minizip"].defines = ["MINIZIP_DLL"]
            self.cpp_info.components["minizip"].requires = ["zlib"]
