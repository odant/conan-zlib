import platform
from conan.packager import ConanMultiPackager

username = "odant"
channel = "stable"
vs_toolset = "v140_xp"

if __name__ == "__main__":
    builder = ConanMultiPackager(username=username, channel=channel)
    if platform.system() == "Windows":
        settings_array = (
        {
            "os": "Windows",
            "compiler": "Visual Studio",
            "compiler.version": 14,
            "compiler.runtime": "MD",
            "compiler.toolset": vs_toolset,
            "build_type": "Release",
            "arch": "x86"
        },
        {
            "os": "Windows",
            "compiler": "Visual Studio",
            "compiler.version": 14,
            "compiler.runtime": "MDd",
            "compiler.toolset": vs_toolset,
            "build_type": "Debug",
            "arch": "x86"
        },
        {
            "os": "Windows",
            "compiler": "Visual Studio",
            "compiler.version": 14,
            "compiler.runtime": "MD",
            "compiler.toolset": vs_toolset,
            "build_type": "Release",
            "arch": "x86_64"
        },
        {
            "os": "Windows",
            "compiler": "Visual Studio",
            "compiler.version": 14,
            "compiler.runtime": "MDd",
            "compiler.toolset": vs_toolset,
            "build_type": "Debug",
            "arch": "x86_64"
        },
        {
            "os": "Windows",
            "compiler": "Visual Studio",
            "compiler.version": 15,
            "compiler.runtime": "MD",
            "compiler.toolset": vs_toolset,
            "build_type": "Release",
            "arch": "x86"
        },
        {
            "os": "Windows",
            "compiler": "Visual Studio",
            "compiler.version": 15,
            "compiler.runtime": "MDd",
            "compiler.toolset": vs_toolset,
            "build_type": "Debug",
            "arch": "x86"
        },
        {
            "os": "Windows",
            "compiler": "Visual Studio",
            "compiler.version": 15,
            "compiler.runtime": "MD",
            "compiler.toolset": vs_toolset,
            "build_type": "Release",
            "arch": "x86_64"
        },
        {
            "os": "Windows",
            "compiler": "Visual Studio",
            "compiler.version": 15,
            "compiler.runtime": "MDd",
            "compiler.toolset": vs_toolset,
            "build_type": "Debug",
            "arch": "x86_64"
        }
        )
    for s in settings_array:
        builder.add(settings=s, options=o)
    builder.run()
