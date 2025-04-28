cmake_minimum_required(VERSION 3.15)
project(PackageTest C)

cmake_policy(SET CMP0028 NEW)

set(COMPONENTS zlib)
if(ENABLE_MINIZIP)
    list(APPEND COMPONENTS minizip)
endif()

find_package(zlib REQUIRED COMPONENTS ${COMPONENTS})

enable_testing()

add_executable(test_zlib test_zlib.c)
target_link_libraries(test_zlib zlib::zlib)
set_target_properties(test_zlib
    PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    BUILD_WITH_INSTALL_RPATH True
)
add_test(
    NAME test_zlib
    COMMAND test_zlib
)

if(ENABLE_MINIZIP)
    add_executable(test_minizip test_minizip.c)
    target_link_libraries(test_minizip zlib::minizip)
    set_target_properties(test_minizip
        PROPERTIES
        INSTALL_RPATH "$ORIGIN"
        BUILD_WITH_INSTALL_RPATH True
    )
    add_test(
        NAME test_minizip
        COMMAND test_minizip
    )
endif()

