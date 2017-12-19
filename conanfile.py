from conans import ConanFile, CMake, tools
import os, glob


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.11"
    license = "http://www.zlib.net/zlib_license.html"
    description = "A Massively Spiffy Yet Delicately Unobtrusive Compression Library " \
                  "(Also Free, Not to Mention Unencumbered by Patents)"
    url = "https://zlib.net/"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [False, True], "minizip": [False, True], "disable_dll_sign": [False, True]}
    default_options = "shared=False", "minizip=True", "disable_dll_sign=False"
    generators = "cmake"
    exports_sources = "src/*", "minizip.patch", "FindZLIB.cmake"
    no_copy_source = True
    build_policy = "missing"
    
    def build_requirements(self):
        if (
                self.settings.os == "Windows" and
                self.settings.build_type == "Release" and
                self.options.shared and
                not self.options.disable_dll_sign
            ):
                self.build_requires("find_windows_signtool/[>=1.0]@%s/stable" % self.user)

    def source(self):
        tools.patch(patch_file="minizip.patch")
	
    def build(self):
        # Build and install to package folder
        cmake = CMake(self, parallel=True)
        source_dir = os.path.join(self.source_folder, "src")        
        defs = {
            "SKIP_INSTALL_FILES:BOOL": True,
            "ENABLE_MINIZIP:BOOL": self.options.minizip
        }
        cmake.configure(source_dir=source_dir, defs=defs)
        cmake.build()
        cmake.install()
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
        if (
                self.settings.os == "Windows" and
                self.settings.build_type == "Release" and
                self.options.shared and
                not self.options.disable_dll_sign
            ):
                with tools.pythonpath(self):
                    from find_windows_signtool import find_signtool
                    signtool = '"' + find_signtool(str(self.settings.arch)) + '"'
                    params =  "sign /a /t http://timestamp.verisign.com/scripts/timestamp.dll"
                    pattern = os.path.join(self.package_folder, "bin", "*.dll")
                    for fpath in glob.glob(pattern):
                        self.output.info("Sign %s" % fpath)
                        cmd = "{} {} {}".format(signtool, params, fpath)
                        self.run(cmd)
        
    def package(self):
        self.copy("FindZLIB.cmake", ".", ".")
        #Packing PDB
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            if self.options.shared:
                pass
            else:
                self.copy("*zlibstatic.pdb", "bin", ".", keep_path=False)
                self.copy("*zlibstaticd.pdb", "bin", ".", keep_path=False)
                self.copy("*minizipstatic.pdb", "bin", ".", keep_path=False)
                self.copy("*minizipstaticd.pdb", "bin", ".", keep_path=False)

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

