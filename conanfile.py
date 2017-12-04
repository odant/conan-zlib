from conans import ConanFile, CMake
import os, glob


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.11"
    license = "http://www.zlib.net/zlib_license.html"
    description = "A Massively Spiffy Yet Delicately Unobtrusive Compression Library " \
                  "(Also Free, Not to Mention Unencumbered by Patents)"
    url = "https://zlib.net/"
    settings = {"os": ["Windows"], "compiler": ["Visual Studio"], "build_type": None, "arch": ["x86", "x86_64"]}
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports_sources = "src/*", "FindZLIB.cmake"
    no_copy_source = True
    build_policy = "missing"
    
    def source(self):
        # Patch CMakeLists.txt, set PDB output name
        txt = """
if(WIN32 AND MSVC)
    set_target_properties(zlib PROPERTIES PDB_NAME_DEBUG zlibd)
    set_target_properties(zlibstatic PROPERTIES COMPILE_PDB_NAME_DEBUG zlibstaticd)
endif()
"""
        cmake_script = os.path.join(self.source_folder, "src", "CMakeLists.txt")
        with open(cmake_script, "a") as fd:
            fd.write(txt)
	
    def build(self):
        # Build and install to package folder
        cmake = CMake(self, parallel=True)
        source_dir = os.path.join(self.source_folder, "src")        
        defs = {"SKIP_INSTALL_FILES:BOOL": "ON"}
        cmake.configure(source_dir=source_dir, defs=defs)
        cmake.build()
        cmake.install()
        # Remove unused files
        if self.options.shared:
            pattern = os.path.join(self.package_folder, "lib", "zlibstatic.*")
            removable = glob.glob(pattern)
        if not self.options.shared:
            pattern = os.path.join(self.package_folder, "bin", "*.dll")
            removable = glob.glob(pattern)
            pattern = os.path.join(self.package_folder, "lib", "*.so*")
            removable += glob.glob(pattern)
        for fpath in removable:
            self.output.info("Remove %s" % fpath)
            os.remove(fpath)
        # Sign DLL
        if self.settings.os == "Windows" and self.settings.build_type == "Release" and self.options.shared:
            signtool = '"C:\\Program Files (x86)\\Microsoft SDKs\\Windows\\v7.1A\\bin\\signtool"'
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
                self.copy("*zlib.pdb", "bin", ".", keep_path=False)
                self.copy("*zlibd.pdb", "bin", ".", keep_path=False)
            else:
                self.copy("*zlibstatic.pdb", "bin", ".", keep_path=False)
                self.copy("*zlibstaticd.pdb", "bin", ".", keep_path=False)

    def package_info(self):
        suffix = ".lib"
        if self.options.shared:
            self.cpp_info.libs = ["zlib"]
        else:
            self.cpp_info.libs = ["zlibstatic"]
        if self.settings.build_type == "Debug":
            self.cpp_info.libs[0] += "d"
