import platform, os, copy
from conan.packager import ConanMultiPackager


# Common settings
username = "odant" if "CONAN_USERNAME" not in os.environ else None
# Windows settings
visual_versions = ["14", "15"] if "CONAN_VISUAL_VERSIONS" not in os.environ else None
visual_runtimes = ["MD", "MDd"] if "CONAN_VISUAL_RUNTIMES" not in os.environ else None
visual_default_toolsets = {
    "14": [None, "v140_xp"],
    "15": [None, "v141_xp"]
}
visual_toolsets = None
if "CONAN_VISUAL_TOOLSETS" in os.environ:
    visual_toolsets = [s.strip() for s in os.environ["CONAN_VISUAL_TOOLSETS"].split(",")]
dll_sign = False if "CONAN_DISABLE_DLL_SIGN" in os.environ else True

def vs_get_toolsets(compiler_version):
    return visual_toolsets if not visual_toolsets is None else visual_default_toolsets.get(compiler_version)
    
def vs_add_toolset_to_build(settings, options, env_vars, build_requires, toolsets):
    result = []
    if toolsets is None:
        result.append([settings, options, env_vars, build_requires])
    else:
        for t in toolsets:
            s = copy.deepcopy(settings)
            s["compiler.toolset"] = t
            result.append([s, options, env_vars, build_requires])
    return result
    
if __name__ == "__main__":
    builder = ConanMultiPackager(
        username=username,
        visual_versions=visual_versions,
        visual_runtimes=visual_runtimes
    )
    builder.add_common_builds(pure_c=True, shared_option_name="zlib:shared")
    if platform.system() == "Windows":
        builds = []
        for settings, options, env_vars, build_requires in builder.builds:
            if settings["compiler"] == "Visual Studio":
                toolsets = vs_get_toolsets(settings["compiler.version"])
                builds += vs_add_toolset_to_build(settings, options, env_vars, build_requires, toolsets)
        for settings, options, env_vars, build_requires in builds:
            options["zlib:dll_sign"] = dll_sign
        builder.builds = builds
    builder.run()
