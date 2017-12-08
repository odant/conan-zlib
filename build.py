import platform, os, copy
from conan.packager import ConanMultiPackager


# Common settings
username = "odant" if "CONAN_USERNAME" not in os.environ else None
# Windows settings
visual_versions = ["14", "15"] if "CONAN_VISUAL_VERSIONS" not in os.environ else None
visual_runtimes = ["MD", "MDd"] if "CONAN_VISUAL_RUNTIMES" not in os.environ else None
visual_toolsets = {
    "14": [None, "v140_xp"],
    "15": [None, "v141_xp"]
}

def vs_add_toolset(settings, options, env_vars, build_requires, toolsets=visual_toolsets):
    compiler_toolsets = toolsets.get(settings["compiler.version"])
    result = []
    if compiler_toolsets is None:
        result.append([settings, options, env_vars, build_requires])
    else:
        for t in compiler_toolsets:
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
    builder.add_common_builds()
    if platform.system() == "Windows":
        builds = []
        for settings, options, env_vars, build_requires in builder.builds:
            if settings["compiler"] == "Visual Studio":
                builds += vs_add_toolset(settings, options, env_vars, build_requires)
        builder.builds = builds
    builder.run()
